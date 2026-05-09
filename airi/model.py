import json
import socket
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from airi.config import MODEL_PROVIDER, OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_OPTIONS


def generate_text(prompt: str) -> str:
    if MODEL_PROVIDER != "ollama":
        return f"Неизвестный MODEL_PROVIDER: {MODEL_PROVIDER}"

    url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate"
    data = json.dumps(
        {
            "model": OLLAMA_MODEL,
            "options": OLLAMA_OPTIONS,
            "prompt": prompt,
            "stream": False,
            "think": False,
        }
    ).encode("utf-8")

    request = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        # timeout нужен, чтобы программа не зависла навсегда при проблемах с Ollama.
        with urlopen(request, timeout=120) as response:
            raw_response = response.read().decode("utf-8")
    except HTTPError as error:
        raw_error = error.read().decode("utf-8", errors="replace")

        try:
            error_data = json.loads(raw_error)
            error_message = error_data.get("error", raw_error)
        except json.JSONDecodeError:
            error_message = raw_error

        if error.code == 404 or "not found" in error_message.lower():
            return (
                f"Модель Ollama не найдена: {OLLAMA_MODEL}. "
                f"Проверь имя модели или скачай ее командой: ollama pull {OLLAMA_MODEL}"
            )

        return f"Ollama вернула ошибку HTTP {error.code}: {error_message}"
    except (URLError, TimeoutError, socket.timeout):
        return (
            "Не удалось подключиться к Ollama. "
            f"Проверь, что Ollama запущена и доступна по адресу {OLLAMA_BASE_URL}."
        )

    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError:
        return "Ollama вернула ответ не в формате JSON."

    if not isinstance(result, dict) or "response" not in result:
        return "Ollama вернула ответ в неожиданном формате."

    response_text = result["response"]

    if not isinstance(response_text, str):
        return "Ollama вернула поле response в неожиданном формате."

    return response_text
