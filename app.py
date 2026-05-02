from airi.brain import generate_response
from airi.memory import init_db


init_db()

print("Привет! Я Airi.")

while True:
    user_message = input("> ")

    if user_message.strip().lower() in ["exit", "quit", "выход"]:
        break

    response = generate_response(user_message)
    print(response)
