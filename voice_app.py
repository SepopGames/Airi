from airi.brain import generate_response
from airi.memory import init_db
from airi.voice.qwen_tts import speak_text


EXIT_COMMANDS = {"exit", "quit", "выход", "/exit", "/quit"}


def guess_emotion(response: str) -> str:
    """
    Простая временная логика выбора эмоции по тексту ответа.

    Это НЕ режим личности.
    Айри остаётся одной и той же, просто голос подстраивается под интонацию.
    """
    text = response.lower()

    angry_markers = [
        "ну ты серьёзно",
        "я же говорила",
        "ошибк",
        "traceback",
        "сломал",
        "сломалось",
    ]

    flirty_markers = [
        "хе-хе",
        "мил",
        "интересно",
        "герой",
        "ну что",
    ]

    if any(marker in text for marker in angry_markers):
        return "angry"

    if any(marker in text for marker in flirty_markers):
        return "horny"

    return "neutral"


def main() -> None:
    init_db()

    print("Airi voice mode запущен.")
    print("Пиши сообщение. /exit — выйти.")
    print("Первый голосовой ответ может быть долгим: Qwen3-TTS грузит модель.")

    while True:
        user_message = input("> ").strip()

        if not user_message:
            continue

        if user_message.lower() in EXIT_COMMANDS:
            print("Airi: Ладно, отключаюсь. Но я рядом.")
            break

        response = generate_response(user_message)
        print(f"Airi: {response}")

        emotion = guess_emotion(response)
        print(f"[voice emotion: {emotion}]")

        speak_text(response, emotion=emotion)


if __name__ == "__main__":
    main()