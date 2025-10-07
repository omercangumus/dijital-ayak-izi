from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal


class SelfScanRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr | None = None


class ScanItem(BaseModel):
    title: str | None = None
    link: str | None = None
    name: str | None = None
    domain: str | None = None
    thumbnail: str | None = None
    source: str
    type: Literal['web', 'breach', 'social', 'image']


class SelfScanResponse(BaseModel):
    query: dict
    results: List[ScanItem]
    offline: bool
    risk_score: int
    risk_level: Literal['dusuk', 'orta', 'yuksek']


