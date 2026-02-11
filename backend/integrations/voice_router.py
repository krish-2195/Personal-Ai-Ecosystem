from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.integrations.voice import synthesize_speech, transcribe_audio


router = APIRouter(prefix="/v1/voice", tags=["voice"])


class TranscribeRequest(BaseModel):
    audio_base64: str = Field(..., min_length=1)


class SynthesizeRequest(BaseModel):
    text: str = Field(..., min_length=1)


@router.post("/transcribe")
def transcribe(request: TranscribeRequest) -> dict:
    result = transcribe_audio(request.audio_base64)
    return {
        "text": result.text,
        "engine": result.engine,
        "simulated": result.simulated,
    }


@router.post("/synthesize")
def synthesize(request: SynthesizeRequest) -> dict:
    result = synthesize_speech(request.text)
    return {
        "audio_base64": result.audio_base64,
        "engine": result.engine,
        "simulated": result.simulated,
    }
