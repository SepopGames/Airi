import wave
from pathlib import Path

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel


PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
STT_INPUT_DIR = PROJECT_DIR / "data" / "stt_input"
STT_INPUT_PATH = STT_INPUT_DIR / "latest_input.wav"

SAMPLE_RATE = 16000
CHANNELS = 1

_model = None


def get_stt_model() -> WhisperModel:
    """
    Загружает Whisper один раз.

    Пока используем CPU int8, чтобы не драться за VRAM с Ollama/Gemma и Qwen3-TTS.
    Потом можно попробовать device='cuda'.
    """
    global _model

    if _model is not None:
        return _model

    print("[STT] Загружаю faster-whisper...")

    _model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8",
    )

    return _model


def record_microphone(duration_seconds: int = 6) -> Path:
    """
    Записывает микрофон в WAV-файл.
    """
    STT_INPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[MIC] Говори. Записываю {duration_seconds} сек...")

    audio = sd.rec(
        int(duration_seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
    )
    sd.wait()

    audio = np.asarray(audio)

    with wave.open(str(STT_INPUT_PATH), "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio.tobytes())

    print(f"[MIC] Запись готова: {STT_INPUT_PATH}")

    return STT_INPUT_PATH


def transcribe_audio(audio_path: Path) -> str:
    """
    Распознаёт речь из WAV-файла.
    """
    model = get_stt_model()

    print("[STT] Распознаю речь...")

    segments, info = model.transcribe(
        str(audio_path),
        language="ru",
        vad_filter=True,
    )

    text_parts = []

    for segment in segments:
        text_parts.append(segment.text.strip())

    text = " ".join(text_parts).strip()

    print(f"[STT] Язык: {info.language}, вероятность: {info.language_probability:.2f}")
    print(f"[STT] Текст: {text}")

    return text


def listen_once(duration_seconds: int = 6) -> str:
    """
    Записать микрофон один раз и вернуть распознанный текст.
    """
    audio_path = record_microphone(duration_seconds=duration_seconds)
    return transcribe_audio(audio_path)