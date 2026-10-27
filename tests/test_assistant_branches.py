import unittest
from datetime import datetime, timezone
from unittest.mock import Mock, patch

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.gemini import (
    GeminiAdvice,
    GeminiNotConfiguredError,
    GeminiRateLimitError,
    GeminiServiceError,
    GeminiTimeoutError,
    GeminiUnavailableError,
)
from app.database import Base
from app.models.ai_conversation import AIConversation, AIMessage
from app.models.user import User
from app.routers.assistant import (
    ask_assistant,
    get_assistant_context,
    list_conversations,
)
from app.schemas.assistant import AssistantAskRequest


class AssistantBranchTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.db = sessionmaker(bind=self.engine)()
        self.user = User(id="u1", username="owner", email="owner@example.com", password_hash="x")
        self.other = User(id="u2", username="other", email="other@example.com", password_hash="x")
        self.db.add_all([self.user, self.other])
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_context_empty_state_and_conversation_summaries(self):
        context = get_assistant_context(month=1, year=2026, db=self.db, current_user=self.user)
        self.assertFalse(context.has_data)
        self.assertEqual(len(context.privacy_notes), 4)

        empty = AIConversation(
            id="empty", user_id=self.user.id, title="Empty",
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            updated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        active = AIConversation(
            id="active", user_id=self.user.id, title="Active",
            created_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
            updated_at=datetime(2026, 1, 3, tzinfo=timezone.utc),
        )
        hidden = AIConversation(id="hidden", user_id=self.other.id, title="Hidden")
        self.db.add_all([empty, active, hidden])
        self.db.add_all([
            AIMessage(
                id="m1", conversation_id=active.id, role="user", content="first",
                created_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
            ),
            AIMessage(
                id="m2", conversation_id=active.id, role="assistant", content="z" * 150,
                created_at=datetime(2026, 1, 3, tzinfo=timezone.utc),
            ),
        ])
        self.db.commit()

        results = list_conversations(self.db, self.user)
        self.assertEqual([item.id for item in results], ["active", "empty"])
        self.assertEqual(results[0].message_count, 2)
        self.assertEqual(results[0].preview, "z" * 120)
        self.assertEqual(results[1].preview, "")

    def test_blank_question_and_long_title(self):
        with self.assertRaises(HTTPException) as caught:
            ask_assistant(AssistantAskRequest(question="   "), self.db, self.user)
        self.assertEqual(caught.exception.status_code, 422)

        question = "q" * 80
        with patch("app.routers.assistant.generate_financial_advice", return_value=GeminiAdvice("answer", "primary")):
            result = ask_assistant(AssistantAskRequest(question=question), self.db, self.user)
        self.assertEqual(result.conversation.title, "q" * 72 + "…")
        self.assertEqual(result.conversation.preview, "answer")

    def test_existing_conversation_passes_history(self):
        conversation = AIConversation(id="thread", user_id=self.user.id, title="Thread")
        self.db.add(conversation)
        self.db.add(AIMessage(id="old", conversation_id="thread", role="user", content="old question"))
        self.db.commit()

        with patch("app.routers.assistant.generate_financial_advice", return_value=GeminiAdvice("new answer", "fallback")) as generate:
            result = ask_assistant(
                AssistantAskRequest(question="new question", conversation_id="thread", month=2, year=2026),
                self.db,
                self.user,
            )
        history = list(generate.call_args.args[2])
        self.assertEqual(history, [("user", "old question")])
        self.assertEqual(result.conversation.message_count, 3)
        self.assertEqual(result.conversation.messages[-1].context_month, 2)

    @patch.dict("os.environ", {"GEMINI_MODEL": "gemini-3.8-flash", "GEMINI_FALLBACK_MODEL": "gemini-3.1-pro-preview"})
    @patch("app.core.gemini._api_key", return_value="test-key")
    @patch("app.core.gemini.time.sleep")
    def test_real_gateway_fallback_persists_once_and_all_busy_rolls_back(self, sleep, key):
        success = Mock(status_code=200)
        success.json.return_value = {"output_text": "Phân tích."}
        with patch("app.core.gemini.requests.post", side_effect=[Mock(status_code=503), Mock(status_code=503), success]):
            result = ask_assistant(AssistantAskRequest(question="Tóm tắt"), self.db, self.user)
        self.assertEqual(result.model, "gemini-3.1-pro-preview")
        self.assertEqual(self.db.query(AIConversation).count(), 1)
        self.assertEqual(self.db.query(AIMessage).count(), 2)
        with patch("app.core.gemini.requests.post", return_value=Mock(status_code=503)):
            with self.assertRaises(HTTPException) as caught:
                ask_assistant(AssistantAskRequest(question="Câu hỏi mới"), self.db, self.user)
        self.assertEqual(caught.exception.status_code, 503)
        self.assertEqual(self.db.query(AIConversation).count(), 1)
        self.assertEqual(self.db.query(AIMessage).count(), 2)

    def test_gemini_exceptions_are_mapped_and_rolled_back(self):
        cases = [
            (GeminiNotConfiguredError("not configured"), 503),
            (GeminiRateLimitError("limited"), 429),
            (GeminiTimeoutError("timeout"), 504),
            (GeminiUnavailableError("down"), 503),
            (GeminiServiceError("bad response"), 502),
        ]
        for exception, status_code in cases:
            with self.subTest(exception=type(exception).__name__), patch(
                "app.routers.assistant.generate_financial_advice", side_effect=exception
            ):
                with self.assertRaises(HTTPException) as caught:
                    ask_assistant(AssistantAskRequest(question="help"), self.db, self.user)
                self.assertEqual(caught.exception.status_code, status_code)
                self.assertEqual(caught.exception.detail, str(exception))
                self.assertEqual(self.db.query(AIConversation).count(), 0)


if __name__ == "__main__":
    unittest.main()
