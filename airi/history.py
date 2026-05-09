from collections import deque


# Максимум сообщений, которые держим в краткосрочной истории.
# Эта история живёт только пока запущена программа.
MAX_HISTORY_MESSAGES = 12

# Очередь с ограниченной длиной.
# Если сообщений станет больше 12, старые автоматически удалятся.
_history = deque(maxlen=MAX_HISTORY_MESSAGES)


def add_message(role: str, text: str) -> None:
    """
    Добавляет сообщение в краткосрочную историю.

    role:
    - "user" — сообщение пользователя
    - "airi" — ответ Айри
    """
    if role not in ("user", "airi"):
        raise ValueError("role должен быть 'user' или 'airi'")

    _history.append((role, text))


def get_recent_history() -> list[tuple[str, str]]:
    """
    Возвращает последние сообщения диалога.
    """
    return list(_history)


def format_history() -> str:
    """
    Превращает историю в текст для prompt.
    """
    if not _history:
        return "- История диалога пока пустая."

    lines = []

    for role, text in _history:
        if role == "user":
            name = "Пользователь"
        else:
            name = "Айри"

        lines.append(f"{name}: {text}")

    return "\n".join(lines)


def clear_history() -> None:
    """
    Очищает краткосрочную историю.
    """
    _history.clear()