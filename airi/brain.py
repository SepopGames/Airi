from airi.memory import add_memory, get_recent_memories
from airi.model import generate_text
from airi.personality import SYSTEM_PROMPT
from airi.history import add_message, clear_history, format_history
from airi.router import Intent, route_message


def build_prompt(user_message: str) -> str:
    # Получаем последние воспоминания из простой SQLite-памяти.
    recent_memories = get_recent_memories()

    # Если воспоминаний нет, показываем понятную заглушку.
    if recent_memories:
        memories_text = "\n".join(f"- {memory}" for memory in recent_memories)
    else:
        memories_text = "- Пока нет воспоминаний."

    dialogue_history = format_history()
    # Собираем учебный prompt из личности Airi, памяти и сообщения пользователя.
    prompt = f"""{SYSTEM_PROMPT}
    [Долгосрочная память]
    {memories_text}
    [Последние сообщения диалога]
    {dialogue_history}
    [Текущее сообщение пользователя]
    {user_message}
    [Задача]
    Ответь как Айри. Учитывай память и последние сообщения, но не выдумывай факты, которых нет.
    """
    return prompt


def generate_response(user_message: str) -> str:
    clean_message = user_message.strip()

    route = route_message(clean_message)

    if route.intent == Intent.CLEAR_HISTORY:
        clear_history()
        return "Краткосрочную историю очистила. Начинаем с чистого листа."

    if route.intent == Intent.REMEMBER:
        memory_text = route.content

        if not memory_text:
            return "Что именно запомнить? Ты дал команду, но не написал сам факт."

        add_memory(memory_text)
        response = f"Запомнила: {memory_text}"

        add_message("user", clean_message)
        add_message("airi", response)

        return response

    if route.intent == Intent.SHOW_MEMORY:
        recent_memories = get_recent_memories()

        if not recent_memories:
            return "Я пока ничего не помню."

        memories_text = "\n".join(f"- {memory}" for memory in recent_memories)
        response = f"Вот что я помню:\n{memories_text}"

        add_message("user", clean_message)
        add_message("airi", response)

        return response

    prompt = build_prompt(clean_message)
    response = generate_text(prompt)

    add_message("user", clean_message)
    add_message("airi", response)

    return response
