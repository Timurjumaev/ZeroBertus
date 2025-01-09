from pydantic import BaseModel


class Token(BaseModel):
    id: int
    access_token: str
    refresh_token: str
    token_type: str
    access_token_expires_in: int
    refresh_token_expires_in: int


class TokenData(BaseModel):
    username: str
