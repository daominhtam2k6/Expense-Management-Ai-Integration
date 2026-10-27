import unittest
from unittest.mock import Mock, patch

import requests

from app.core.gemini import (
    GeminiTimeoutError,
    GeminiUnavailableError,
    GeminiServiceError,
    GeminiAdvice,
    configured_model,
    configured_fallback_model,
    extract_response_text,
    generate_financial_advice,
)


class GeminiResponseParsingTests(unittest.TestCase):
    def test_default_model_pair(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(configured_model(), "gemini-3.8-flash")
            self.assertEqual(configured_fallback_model(), "gemini-3.1-pro-preview")

    def test_extracts_sdk_output_text(self):
        self.assertEqual(extract_response_text({"output_text": "  Xin chào  "}), "Xin chào")

    def test_extracts_raw_interactions_model_output(self):
        payload = {
            "status": "completed",
            "steps": [
                {
                    "type": "model_output",
                    "content": [
                        {"type": "text", "text": "Kết luận."},
                        {"type": "text", "text": "Bằng chứng."},
                    ],
                }
            ],
        }
        self.assertEqual(extract_response_text(payload), "Kết luận.\nBằng chứng.")

    def test_ignores_non_text_steps(self):
        self.assertEqual(
            extract_response_text({"steps": [{"type": "tool_call", "content": []}]}),
            "",
        )

    @patch("app.core.gemini.time.sleep")
    @patch("app.core.gemini.requests.post")
    @patch("app.core.gemini._api_key", return_value="test-key")
    def test_retries_transient_upstream_failure(self, _key, post, sleep):
        busy = Mock(status_code=503)
        success = Mock(status_code=200)
        success.json.return_value = {"output_text": "Đã phân tích."}
        post.side_effect = [busy, success]

        result = generate_financial_advice("Tóm tắt", {}, [])

        self.assertEqual(result.text, "Đã phân tích.")
        self.assertEqual(post.call_count, 2)
        self.assertEqual(sleep.call_count, 1)
        self.assertGreaterEqual(sleep.call_args.args[0], 1)
        self.assertLessEqual(sleep.call_args.args[0], 1.5)
        generation_config = post.call_args.kwargs["json"]["generation_config"]
        self.assertEqual(generation_config["thinking_level"], "low")
        self.assertNotIn("temperature", generation_config)

    @patch("app.core.gemini.requests.post", side_effect=requests.ReadTimeout())
    @patch("app.core.gemini._api_key", return_value="test-key")
    def test_reports_timeout_separately(self, _key, _post):
        with self.assertRaises(GeminiTimeoutError):
            generate_financial_advice("Tóm tắt", {}, [])


@patch.dict("os.environ", {"GEMINI_MODEL": "primary", "GEMINI_FALLBACK_MODEL": "fallback"})
@patch("app.core.gemini._api_key", return_value="test-key")
@patch("app.core.gemini.time.sleep")
class GeminiFallbackTests(unittest.TestCase):
    def success(self):
        response = Mock(status_code=200)
        response.json.return_value = {"output_text": "Kết quả."}
        return response

    def test_503_falls_back_with_same_prompt_and_actual_model(self, sleep, key):
        responses = [Mock(status_code=503), Mock(status_code=503), self.success()]
        with patch("app.core.gemini.requests.post", side_effect=responses) as post:
            result = generate_financial_advice("Câu hỏi", {"total": 123}, iter([("user", "Lịch sử")]))
        self.assertEqual(result, GeminiAdvice("Kết quả.", "fallback"))
        payloads = [call.kwargs["json"] for call in post.call_args_list]
        self.assertEqual([p["model"] for p in payloads], ["primary", "primary", "fallback"])
        self.assertEqual(len({p["input"] for p in payloads}), 1)
        self.assertIn("Lịch sử", payloads[-1]["input"])
        self.assertTrue(all(p["store"] is False for p in payloads))
        for response in responses:
            response.close.assert_called_once()

    def test_primary_success_does_not_call_fallback(self, sleep, key):
        with patch("app.core.gemini.requests.post", return_value=self.success()) as post:
            result = generate_financial_advice("q", {}, [])
        self.assertEqual(result.model, "primary")
        self.assertEqual(post.call_count, 1)
        sleep.assert_not_called()

    def test_all_models_busy_raise_unavailable(self, sleep, key):
        with patch("app.core.gemini.requests.post", return_value=Mock(status_code=503)) as post:
            with self.assertRaises(GeminiUnavailableError):
                generate_financial_advice("q", {}, [])
        self.assertEqual(post.call_count, 3)

    def test_timeout_switches_directly_to_fallback(self, sleep, key):
        with patch("app.core.gemini.requests.post", side_effect=[requests.ReadTimeout(), self.success()]) as post:
            result = generate_financial_advice("q", {}, [])
        self.assertEqual(result.model, "fallback")
        self.assertEqual(post.call_count, 2)
        sleep.assert_not_called()

    def test_client_errors_do_not_retry_or_fallback(self, sleep, key):
        for status in (400, 401, 403, 404):
            with self.subTest(status=status), patch("app.core.gemini.requests.post", return_value=Mock(status_code=status)) as post:
                with self.assertRaises(GeminiServiceError):
                    generate_financial_advice("q", {}, [])
                self.assertEqual(post.call_count, 1)
        sleep.assert_not_called()

    def test_empty_or_duplicate_fallback_is_skipped(self, sleep, key):
        for model in ("", "primary"):
            with self.subTest(model=model), patch.dict("os.environ", {"GEMINI_FALLBACK_MODEL": model}), patch(
                "app.core.gemini.requests.post", return_value=Mock(status_code=503)
            ) as post:
                with self.assertRaises(GeminiUnavailableError):
                    generate_financial_advice("q", {}, [])
                self.assertEqual(post.call_count, 2)

    def test_expired_budget_stops_additional_calls(self, sleep, key):
        with patch("app.core.gemini.time.monotonic", side_effect=[0, 0, 61]), patch(
            "app.core.gemini.requests.post", return_value=Mock(status_code=503)
        ) as post:
            with self.assertRaises(GeminiTimeoutError):
                generate_financial_advice("q", {}, [])
        self.assertEqual(post.call_count, 1)
        sleep.assert_not_called()

    def test_remaining_budget_limits_transport_timeout(self, sleep, key):
        with patch("app.core.gemini.time.monotonic", side_effect=[0, 58, 59]), patch(
            "app.core.gemini.requests.post", return_value=self.success()
        ) as post:
            generate_financial_advice("q", {}, [])
        timeout = post.call_args.kwargs["timeout"]
        self.assertEqual(timeout.total, 2)
        self.assertEqual(timeout.connect_timeout, 2)


if __name__ == "__main__":
    unittest.main()
