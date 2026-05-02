from airi.personality import SYSTEM_PROMPT
from airi.memory import add_memory, get_recent_memories


def build_prompt(user_message: str) -> str:
    # Получаем последние воспоминания из простой SQLite-памяти.
    recent_memories = get_recent_memories()

    # Если воспоминаний нет, показываем понятную заглушку.
    if recent_memories:
        memories_text = "\n".join(f"- {memory}" for memory in recent_memories)
    else:
        memories_text = "- Пока нет воспоминаний."

    # Собираем учебный prompt из личности Airi, памяти и сообщения пользователя.
    prompt = f"""{SYSTEM_PROMPT}

Последние воспоминания:
{memories_text}

Сообщение пользователя:
{user_message}
"""

    return prompt


def fake_llm_response(prompt: str, user_message: str) -> str:
    # prompt пока не отправляется в настоящую LLM, но уже собирается для будущего.
    lower_message = user_message.lower()

    # Простая проверка вопроса про память.
    if "что ты помнишь" in lower_message:
        recent_memories = get_recent_memories()

        if not recent_memories:
            return "Я пока ничего не помню."

        memories_text = "\n".join(f"- {memory}" for memory in recent_memories)
        return f"Вот что я помню:\n{memories_text}"

    # Временный простой ответ в стиле Airi без подключения настоящей модели.
    return f"Я рядом и слышу тебя. Ты написал: {user_message}"


def generate_response(user_message: str) -> str:
    # Убираем лишние пробелы по краям, чтобы команды читались проще.
    clean_message = user_message.strip()

    # Команда "запомни" сохраняет текст после этого слова в память.
    if clean_message.lower().startswith("запомни"):
        memory_text = clean_message[len("запомни") :].strip()
        if not memory_text:
            return "Что именно запомнить? Ты дал команду, но не написал сам факт."
        add_memory(memory_text)
        return f"Запомнила: {memory_text}"
    
    

    # Для обычных сообщений собираем prompt и передаем его в фейковый ответ.
    prompt = build_prompt(clean_message)
    return fake_llm_response(prompt, clean_message)
