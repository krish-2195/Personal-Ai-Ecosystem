from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.profiles.store import Profile, get_profile, update_profile


router = APIRouter(prefix="/v1/profile", tags=["profile"])


class ProfileResponse(BaseModel):
    id: str
    display_name: str
    timezone: str
    privacy_mode: str
    data_retention_days: int
    local_only: bool


class ProfileUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1)
    timezone: str | None = Field(default=None, min_length=1)
    privacy_mode: str | None = Field(default=None, pattern="^(strict|balanced|open)$")
    data_retention_days: int | None = Field(default=None, ge=1, le=3650)
    local_only: bool | None = None


@router.get("", response_model=ProfileResponse)
def get_default_profile() -> ProfileResponse:
    profile: Profile = get_profile()
    return ProfileResponse(**profile.__dict__)


@router.patch("", response_model=ProfileResponse)
def patch_profile(request: ProfileUpdate) -> ProfileResponse:
    payload = request.model_dump(exclude_none=True)
    profile = update_profile(payload)
    return ProfileResponse(**profile.__dict__)
