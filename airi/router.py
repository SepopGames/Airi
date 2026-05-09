from dataclasses import dataclass
from enum import Enum


class Intent(str, Enum):
    REMEMBER = "remember"
    SHOW_MEMORY = "show_memory"
    CLEAR_HISTORY = "clear_history"
    CHAT = "chat"
    SEARCH_MEMORY = "search_memory"
    FORGET_MEMORY = "forget_memory"


@dataclass
class RouteResult:
    intent: Intent
    content: str


def clean_remember_text(message: str) -> str:
    """
    Убирает командную часть из фразы "запомни ...".

    Примеры:
    "запомни что меня зовут Ильяс" -> "меня зовут Ильяс"
    "запомни, что я учу ML" -> "я учу ML"
    "запомни: Саша любит шутки" -> "Саша любит шутки"
    """
    text = message.strip()

    lower_text = text.lower()

    if lower_text.startswith("запомни"):
        text = text[len("запомни"):].strip()

    # Убираем частые разделители после команды.
    text = text.lstrip(" ,:—-").strip()

    # Убираем лишнее "что" в начале.
    if text.lower().startswith("что "):
        text = text[4:].strip()

    return text


def route_message(message: str) -> RouteResult:
    """
    Определяет намерение пользователя:
    - сохранить память
    - показать память
    - очистить историю
    - обычный чат
    """
    clean_message = message.strip()
    lower_message = clean_message.lower()

    if lower_message in {"/clear", "clear", "очисти историю"}:
        return RouteResult(Intent.CLEAR_HISTORY, "")

    if lower_message in {"/memory", "memory", "память"}:
        return RouteResult(Intent.SHOW_MEMORY, "")

    if "что ты помнишь" in lower_message:
        return RouteResult(Intent.SHOW_MEMORY, "")

    if lower_message.startswith("запомни"):
        memory_text = clean_remember_text(clean_message)
        return RouteResult(Intent.REMEMBER, memory_text)
    
    if lower_message.startswith("/search "):
        query = clean_message[len("/search "):].strip()
        return RouteResult(Intent.SEARCH_MEMORY, query)

    if lower_message.startswith("/forget "):
        memory_id = clean_message[len("/forget "):].strip()
        return RouteResult(Intent.FORGET_MEMORY, memory_id)
    
    return RouteResult(Intent.CHAT, clean_message)