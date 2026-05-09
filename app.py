from airi.brain import generate_response
from airi.memory import init_db


EXIT_COMMANDS = {"exit", "quit", "выход", "/exit", "/quit"}


def main() -> None:
    init_db()

    print("Привет! Я Airi.")
    print("Напиши /exit, чтобы выйти.")

    while True:
        user_message = input("> ").strip()

        if not user_message:
            continue

        if user_message.lower() in EXIT_COMMANDS:
            print("Airi: Ладно, отключаюсь. Но я рядом, если что.")
            break

        response = generate_response(user_message)
        print(f"Airi: {response}")


if __name__ == "__main__":
    main()
