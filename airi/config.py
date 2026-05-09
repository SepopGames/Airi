MODEL_PROVIDER = "ollama"

OLLAMA_BASE_URL = "http://localhost:11434"

OLLAMA_MODEL = "gemma4:26b"

# Настройки генерации Ollama.
# temperature: выше = креативнее, ниже = стабильнее.
# top_p: ограничивает выбор токенов, помогает держать ответ в адекватных рамках.
# num_predict: максимальная длина ответа в токенах.
# num_ctx: размер контекста, сколько текста модель может учитывать.
# repeat_penalty: штраф за повторы.
OLLAMA_OPTIONS = {
    "temperature": 0.8,
    "top_p": 0.9,
    "num_predict": 500,
    "num_ctx": 8192,
    "repeat_penalty": 1.1,
}