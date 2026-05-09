from airi.memory import add_memory, get_recent_memories
from airi.model import generate_text
from airi.personality import SYSTEM_PROMPT
from airi.history import add_message, format_history


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
    # Убираем лишние пробелы по краям, чтобы команды читались проще.
    clean_message = user_message.strip()
    lower_message = clean_message.lower()

    # Команда "запомни" сохраняет текст после этого слова в память.
    if lower_message.startswith("запомни"):
        memory_text = clean_message[len("запомни") :].strip()

        if not memory_text:
            return "Что именно запомнить? Ты дал команду, но не написал сам факт."

        add_memory(memory_text)
        response = f"Запомнила: {memory_text}"

        add_message("user", clean_message)
        add_message("airi", response)

        return response

    # Вопрос про память пока обрабатываем здесь, без настоящей модели.
    if "что ты помнишь" in lower_message:
        recent_memories = get_recent_memories()

        if not recent_memories:
            return "Я пока ничего не помню."

        memories_text = "\n".join(f"- {memory}" for memory in recent_memories)
        return f"Вот что я помню:\n{memories_text}"

    # Для обычных сообщений собираем prompt и передаем его в fake-модель.
    prompt = build_prompt(clean_message)
    response = generate_text(prompt)

    add_message("user", clean_message)
    add_message("airi", response)

    return response
