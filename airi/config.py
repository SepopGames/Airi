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

# TTS-настройки.
TTS_ENABLED = True
TTS_PROVIDER = "qwen3"

# Qwen3-TTS.
QWEN_TTS_MODEL = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"

# Папки с локальными голосами и результатами.
# Эти папки НЕ должны попадать на GitHub.
QWEN_TTS_REF_DIR = "data/voice_refs/qwen"
QWEN_TTS_OUTPUT_DIR = "data/tts_output/qwen3_runtime"

# Эмоция по умолчанию.
QWEN_TTS_DEFAULT_EMOTION = "neutral"

# Эмоции, которые реально есть локально:
# neutral.wav + neutral.txt
# angry.wav + angry.txt
# horny.wav + horny.txt
QWEN_TTS_AVAILABLE_EMOTIONS = ["neutral", "angry", "horny"]