import os
import time
from pathlib import Path
from typing import Any

from airi.config import (
    QWEN_TTS_AVAILABLE_EMOTIONS,
    QWEN_TTS_DEFAULT_EMOTION,
    QWEN_TTS_MODEL,
    QWEN_TTS_OUTPUT_DIR,
    QWEN_TTS_REF_DIR,
    TTS_ENABLED,
)


PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
REFERENCE_DIR = PROJECT_DIR / QWEN_TTS_REF_DIR
OUTPUT_DIR = PROJECT_DIR / QWEN_TTS_OUTPUT_DIR

_model = None
_voice_prompts: dict[str, Any] = {}


def get_model():
    """
    Загружает Qwen3-TTS один раз и переиспользует модель.

    Важно:
    - импорт torch/qwen_tts внутри функции, чтобы весь проект не падал,
      если TTS-зависимости не установлены в обычном окружении.
    - модель тяжёлая, поэтому нельзя грузить её на каждый ответ.
    """
    global _model

    if _model is not None:
        return _model

    import torch
    from qwen_tts import Qwen3TTSModel

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA недоступна. Qwen3-TTS лучше запускать на видеокарте.")

    print("[QWEN TTS] Загружаю модель...")
    print("[QWEN TTS] GPU:", torch.cuda.get_device_name(0))

    _model = Qwen3TTSModel.from_pretrained(
        QWEN_TTS_MODEL,
        device_map="cuda:0",
        dtype=torch.bfloat16,
    )

    return _model


def normalize_emotion(emotion: str | None) -> str:
    """
    Проверяет эмоцию и возвращает безопасное значение.

    Если попросили неизвестную эмоцию — используем neutral.
    """
    if not emotion:
        return QWEN_TTS_DEFAULT_EMOTION

    emotion = emotion.strip().lower()

    if emotion not in QWEN_TTS_AVAILABLE_EMOTIONS:
        return QWEN_TTS_DEFAULT_EMOTION

    return emotion


def get_reference_paths(emotion: str) -> tuple[Path, Path]:
    """
    Возвращает путь к wav и txt для выбранной эмоции.
    """
    audio_path = REFERENCE_DIR / f"{emotion}.wav"
    text_path = REFERENCE_DIR / f"{emotion}.txt"

    if not audio_path.exists():
        raise FileNotFoundError(f"Не найден аудиореференс: {audio_path}")

    if not text_path.exists():
        raise FileNotFoundError(f"Не найден текст референса: {text_path}")

    return audio_path, text_path


def get_voice_prompt(emotion: str):
    """
    Создаёт и кэширует voice clone prompt для эмоции.

    Это нужно, чтобы не пересчитывать голосовой профиль каждый раз.
    """
    if emotion in _voice_prompts:
        return _voice_prompts[emotion]

    model = get_model()

    reference_audio, reference_text_path = get_reference_paths(emotion)
    reference_text = reference_text_path.read_text(encoding="utf-8").strip()

    if not reference_text:
        raise ValueError(f"Пустой txt-файл референса: {reference_text_path}")

    print(f"[QWEN TTS] Создаю voice prompt для эмоции: {emotion}")

    voice_prompt = model.create_voice_clone_prompt(
        ref_audio=str(reference_audio),
        ref_text=reference_text,
        x_vector_only_mode=False,
    )

    _voice_prompts[emotion] = voice_prompt
    return voice_prompt


def generate_speech_file(text: str, emotion: str | None = None) -> Path:
    """
    Генерирует wav-файл с голосом Айри и возвращает путь к нему.
    """
    if not TTS_ENABLED:
        raise RuntimeError("TTS выключен в config.py")

    clean_text = text.strip()

    if not clean_text:
        raise ValueError("Нельзя озвучить пустой текст.")

    emotion = normalize_emotion(emotion)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    import soundfile as sf

    model = get_model()
    voice_prompt = get_voice_prompt(emotion)

    timestamp = int(time.time() * 1000)
    output_path = OUTPUT_DIR / f"airi_{emotion}_{timestamp}.wav"

    print(f"[QWEN TTS] Генерирую речь. emotion={emotion}")

    wavs, sample_rate = model.generate_voice_clone(
        text=clean_text,
        language="Russian",
        voice_clone_prompt=voice_prompt,
        max_new_tokens=2048,
        temperature=0.7,
        top_p=0.85,
    )

    sf.write(str(output_path), wavs[0], sample_rate)

    return output_path


def play_audio_file(audio_path: Path) -> None:
    """
    Проигрывает wav-файл.

    На Windows используем os.startfile — просто и без лишних зависимостей.
    Позже заменим на нормальный audio playback без открытия плеера.
    """
    os.startfile(audio_path)


def speak_text(text: str, emotion: str | None = None) -> None:
    """
    Главная функция озвучки.

    Её потом будет вызывать app.py или Discord-бот.
    """
    if not TTS_ENABLED:
        return

    clean_text = text.strip()

    if not clean_text:
        return

    try:
        audio_path = generate_speech_file(clean_text, emotion=emotion)
        play_audio_file(audio_path)
    except Exception as error:
        print(f"[QWEN TTS ERROR] {error}")