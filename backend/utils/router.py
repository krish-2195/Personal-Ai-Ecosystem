from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.utils.scaledown import compress_text


router = APIRouter(prefix="/v1/utils", tags=["utils"])


class CompressRequest(BaseModel):
    text: str = Field(..., min_length=1)


@router.post("/compress")
def compress(request: CompressRequest) -> dict:
    result = compress_text(request.text)
    return {
        "ok": result.ok,
        "ratio": result.ratio,
        "original_size": result.original_size,
        "compressed_size": result.compressed_size,
        "summary": result.summary,
    }
