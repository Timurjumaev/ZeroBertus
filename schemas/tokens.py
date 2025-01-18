from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    id: Optional[int] = None  # ixtiyoriy qilib qo'yilgan
    access_token: str
    refresh_token: Optional[str] = None  # ixtiyoriy qilib qo'yilgan
    token_type: str
    access_token_expires_in: Optional[int] = None  # ixtiyoriy qilib qo'yilgan
    refresh_token_expires_in: Optional[int] = None  # ixtiyoriy qilib qo'yilgan


class TokenData(BaseModel):
    username: str
