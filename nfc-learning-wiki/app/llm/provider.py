"""OpenAI-compatible Chat Completions adapter; secrets stay out of logs/errors."""
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ProviderError(RuntimeError):
    """Safe-to-display provider failure without request secrets or response bodies."""


def load_dotenv(path: Path = Path(".env")) -> None:
    """Load simple KEY=VALUE entries without overriding existing environment values."""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if value[:1] == value[-1:] and value.startswith(("'", '"')):
            value = value[1:-1]
        if key:
            os.environ.setdefault(key, value)


class OpenAICompatibleProvider:
    def __init__(self, *, api_key: str, model: str, base_url: str,
                 timeout: float = 90.0, opener=urlopen):
        if not api_key.strip() or not model.strip():
            raise ValueError("必須設定 NFC_LLM_API_KEY 與 NFC_LLM_MODEL")
        self._api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._opener = opener

    @classmethod
    def from_env(cls, *, dotenv_path: Path = Path(".env"), opener=urlopen):
        load_dotenv(dotenv_path)
        return cls(
            api_key=os.environ.get("NFC_LLM_API_KEY", ""),
            model=os.environ.get("NFC_LLM_MODEL", ""),
            base_url=os.environ.get("NFC_LLM_BASE_URL", "https://api.openai.com/v1"),
            timeout=float(os.environ.get("NFC_LLM_TIMEOUT", "90")),
            opener=opener,
        )

    def complete_json(self, system_prompt: str, user_prompt: str) -> dict:
        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        }).encode("utf-8")
        request = Request(
            f"{self.base_url}/chat/completions", data=payload, method="POST",
            headers={"Authorization": f"Bearer {self._api_key}",
                     "Content-Type": "application/json", "Accept": "application/json"},
        )
        try:
            with self._opener(request, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise ProviderError(f"LLM API 回應 HTTP {exc.code}") from None
        except (URLError, TimeoutError, OSError) as exc:
            # Do not include request headers, API key, or provider response in surfaced errors.
            raise ProviderError(f"LLM API 連線失敗（{type(exc).__name__}）") from None
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ProviderError("LLM API 回傳無法解析的 JSON") from None
        try:
            content = result["choices"][0]["message"]["content"]
            parsed = json.loads(content)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError):
            raise ProviderError("LLM API 未回傳有效的 JSON 物件") from None
        if not isinstance(parsed, dict):
            raise ProviderError("LLM API JSON 頂層必須是物件")
        return parsed
