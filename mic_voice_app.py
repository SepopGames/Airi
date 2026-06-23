from airi.brain import generate_response
from airi.memory import init_db
from airi.voice.qwen_tts import speak_text
from airi.voice.stt import listen_once


EXIT_COMMANDS = {"exit", "quit", "выход", "/exit", "/quit"}


def guess_emotion(response: str) -> str:
    """
    Временный выбор эмоции для голоса.
    Айри остаётся одной личностью, мы меняем только интонацию.
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
        "ну что",
        "герой",
        "интересно",
    ]

    if any(marker in text for marker in angry_markers):
        return "angry"

    if any(marker in text for marker in flirty_markers):
        return "horny"

    return "neutral"


def main() -> None:
    init_db()

    print("Airi microphone voice mode запущен.")
    print("Enter — записать голос.")
    print("Напиши /exit и нажми Enter — выйти.")
    print("Первый запуск STT/TTS может быть долгим: модели грузятся.")

    while True:
        command = input("\nНажми Enter, чтобы говорить > ").strip()

        if command.lower() in EXIT_COMMANDS:
            print("Airi: Отключаю микрофонный режим.")
            break

        user_text = listen_once(duration_seconds=6)

        if not user_text:
            print("Airi: Я ничего не расслышала. Попробуй ещё раз.")
            continue

        print(f"Ты: {user_text}")

        response = generate_response(user_text)
        print(f"Airi: {response}")

        emotion = guess_emotion(response)
        print(f"[voice emotion: {emotion}]")

        speak_text(response, emotion=emotion)


if __name__ == "__main__":
    main()