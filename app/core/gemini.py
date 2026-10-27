import json
import logging
import os
import random
import time
from dataclasses import dataclass
from typing import Iterable

from urllib3.util import Timeout

import requests


DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
DEFAULT_GEMINI_FALLBACK_MODEL = "gemini-3.1-pro-preview"
GEMINI_CONNECT_TIMEOUT = 5
GEMINI_READ_TIMEOUT = 20
GEMINI_REQUEST_BUDGET = 60
GEMINI_MAX_ATTEMPTS = 2

logger = logging.getLogger(__name__)


class GeminiNotConfiguredError(RuntimeError):
    pass


class GeminiServiceError(RuntimeError):
    pass


class GeminiRateLimitError(GeminiServiceError):
    pass


class GeminiTimeoutError(GeminiServiceError):
    pass


class GeminiUnavailableError(GeminiServiceError):
    pass


SYSTEM_INSTRUCTION = """Bạn là trợ lý tài chính cá nhân của Sổ Chi Tiêu.
Chỉ đưa ra giải thích và đề xuất tham khảo; không nói rằng bạn đã hoặc có thể sửa dữ liệu.
Chỉ sử dụng các số liệu tổng hợp trong CONTEXT. Không suy đoán giao dịch, ghi chú, danh tính hoặc thông tin không có trong CONTEXT.
Trả lời bằng tiếng Việt, mở đầu bằng kết luận ngắn, sau đó nêu bằng chứng và giả định khi có dự báo.
Phân biệt rõ dữ liệu thực tế với ước tính. Nếu dữ liệu ít, nói rõ mức độ không chắc chắn.
Không đưa ra lời khuyên đầu tư, tín dụng, thuế hoặc pháp lý mang tính quyết định.
Không dùng HTML. Không nhắc lại dữ liệu riêng tư vì dữ liệu đó không được cung cấp."""


@dataclass(frozen=True)
class GeminiAdvice:
    text: str
    model: str


def configured_model() -> str:
    return os.getenv("GEMINI_MODEL", "").strip() or DEFAULT_GEMINI_MODEL


def configured_fallback_model() -> str:
    # An explicitly empty value disables fallback.
    return os.getenv("GEMINI_FALLBACK_MODEL", DEFAULT_GEMINI_FALLBACK_MODEL).strip()


def _api_key() -> str:
    return (os.getenv("GEMINI_API_KEY") or os.getenv("AI_API_KEY") or "").strip()


def _json_default(value):
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def build_prompt(question: str, context: dict, history: Iterable[tuple[str, str]]) -> str:
    history_lines = []
    for role, content in list(history)[-10:]:
        safe_role = "Người dùng" if role == "user" else "Trợ lý"
        history_lines.append(f"{safe_role}: {content[:2000]}")
    history_text = "\n".join(history_lines) or "Chưa có hội thoại trước đó."
    context_text = json.dumps(context, ensure_ascii=False, default=_json_default, separators=(",", ":"))
    return (
        "LỊCH SỬ HỘI THOẠI TRONG ỨNG DỤNG:\n"
        f"{history_text}\n\n"
        "CONTEXT DỮ LIỆU TỔNG HỢP ĐÃ ẨN DANH:\n"
        f"{context_text}\n\n"
        "CÂU HỎI MỚI:\n"
        f"{question.strip()}"
    )


def extract_response_text(payload: dict) -> str:
    """Read text from both SDK-shaped and raw REST Interactions responses."""
    output_text = payload.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    for step in reversed(payload.get("steps") or []):
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        texts = [
            item.get("text", "").strip()
            for item in step.get("content") or []
            if isinstance(item, dict)
            and item.get("type") == "text"
            and isinstance(item.get("text"), str)
            and item.get("text", "").strip()
        ]
        if texts:
            return "\n".join(texts)

    for output in reversed(payload.get("outputs") or []):
        if not isinstance(output, dict):
            continue
        text = output.get("text")
        if isinstance(text, str) and text.strip():
            return text.strip()
    return ""


def generate_financial_advice(
    question: str, context: dict, history: Iterable[tuple[str, str]]
) -> GeminiAdvice:
    api_key = _api_key()
    if not api_key:
        logger.warning("Gemini API key is not configured")
        raise GeminiNotConfiguredError("Gemini chưa được cấu hình trên máy chủ.")

    # Materialize history once: callers may supply a one-shot generator.
    prompt = build_prompt(question, context, history)
    primary = configured_model()
    fallback = configured_fallback_model()
    models = [primary]
    if fallback and fallback != primary:
        models.append(fallback)
    deadline = time.monotonic() + GEMINI_REQUEST_BUDGET
    last_error = GeminiUnavailableError(
        "Gemini đang tạm thời quá tải hoặc bảo trì. Vui lòng thử lại sau ít phút."
    )

    for model_index, model in enumerate(models):
        # One retry on the primary; one call to the fallback (three calls at most).
        attempts = GEMINI_MAX_ATTEMPTS if model_index == 0 else 1
        payload = {
            "model": model,
            "system_instruction": SYSTEM_INSTRUCTION,
            "input": prompt,
            "store": False,
            "generation_config": {"thinking_level": "low", "max_output_tokens": 900},
        }
        for attempt in range(1, attempts + 1):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise GeminiTimeoutError("Gemini phản hồi quá thời gian chờ. Vui lòng thử lại sau ít phút.")
            response = None
            try:
                response = requests.post(
                    GEMINI_ENDPOINT,
                    headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
                    json=payload,
                    timeout=Timeout(
                        total=min(GEMINI_READ_TIMEOUT, remaining),
                        connect=min(GEMINI_CONNECT_TIMEOUT, remaining),
                        read=min(GEMINI_READ_TIMEOUT, remaining),
                    ),
                    allow_redirects=False,
                )
            except requests.Timeout:
                logger.warning("Gemini timeout model=%s attempt=%s", model, attempt)
                last_error = GeminiTimeoutError(
                    "Gemini phản hồi quá thời gian chờ. Vui lòng thử lại sau ít phút."
                )
                # Reserve the remaining budget for a different model.
                break
            except requests.ConnectionError:
                logger.warning("Gemini connection failed model=%s attempt=%s", model, attempt)
                last_error = GeminiUnavailableError(
                    "Không thể kết nối tới Gemini. Vui lòng thử lại sau ít phút."
                )
            except requests.RequestException as exc:
                logger.warning("Gemini request failed: %s", type(exc).__name__)
                raise GeminiServiceError("Không thể gửi yêu cầu tới Gemini.") from exc

            if time.monotonic() >= deadline:
                if response is not None:
                    response.close()
                raise GeminiTimeoutError("Gemini phản hồi quá thời gian chờ. Vui lòng thử lại sau ít phút.")
            if response is not None:
                try:
                    upstream_status = response.status_code
                    if upstream_status not in (408, 429, 500, 502, 503, 504):
                        if not 200 <= upstream_status < 300:
                            logger.warning("Gemini rejected request model=%s status=%s", model, upstream_status)
                            raise GeminiServiceError(
                                "Gemini từ chối yêu cầu. Hãy kiểm tra khóa API và model cấu hình."
                            )
                        try:
                            body = response.json()
                            if not isinstance(body, dict):
                                raise ValueError("Expected an object")
                            answer = extract_response_text(body)
                        except (ValueError, TypeError, AttributeError) as exc:
                            raise GeminiServiceError("Gemini trả về phản hồi không hợp lệ.") from exc
                        if not answer:
                            raise GeminiServiceError("Gemini chưa tạo được câu trả lời. Vui lòng thử lại.")
                        logger.info("Gemini completed model=%s fallback=%s", model, model_index > 0)
                        return GeminiAdvice(text=answer, model=model)
                    logger.warning("Gemini upstream error model=%s status=%s attempt=%s", model, upstream_status, attempt)
                    if upstream_status == 429:
                        last_error = GeminiRateLimitError(
                            "Gemini đã đạt giới hạn yêu cầu. Vui lòng chờ một lúc rồi thử lại."
                        )
                    else:
                        last_error = GeminiUnavailableError(
                            "Gemini đang tạm thời quá tải hoặc bảo trì. Vui lòng thử lại sau ít phút."
                        )
                finally:
                    response.close()
            if attempt < attempts:
                delay = 2 ** (attempt - 1) + random.uniform(0, 0.5)
                if deadline - time.monotonic() <= delay:
                    raise last_error
                time.sleep(delay)
        if model_index + 1 < len(models):
            logger.warning("Gemini switching to fallback model=%s", models[model_index + 1])
    raise last_error
