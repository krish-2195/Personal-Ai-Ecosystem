from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class TranscriptionResult:
    text: str
    engine: str
    simulated: bool


@dataclass
class SynthesisResult:
    audio_base64: str
    engine: str
    simulated: bool


def transcribe_audio(_: str) -> TranscriptionResult:
    return TranscriptionResult(
        text="(simulated transcription)",
        engine="faster-whisper",
        simulated=True,
    )


def synthesize_speech(text: str) -> SynthesisResult:
    fake_audio = "RkFLRV9XQVY="
    return SynthesisResult(
        audio_base64=fake_audio,
        engine="xtts",
        simulated=True,
    )
