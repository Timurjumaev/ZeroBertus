from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session
from db import database
from models.users import Users
from schemas.tokens import Token

# Security configurations
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Router for login and token management
login_router = APIRouter(tags=['Authentication'])


# Utility functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, expires_delta: Optional[timedelta], token_type: str) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, expected_type: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def get_current_user(db: Session = Depends(database), token: str = Depends(oauth2_scheme)):
    payload = decode_token(token, "access")
    username: Optional[str] = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


# Authentication endpoints
@login_router.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(database), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(Users).filter(Users.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_token(
        data={"sub": user.username}, expires_delta=access_token_expires, token_type="access"
    )
    refresh_token = create_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires, token_type="refresh"
    )

    # Tokenlarni foydalanuvchining jadvaliga yozib qo'yamiz
    user.access_token = access_token
    user.refresh_token = refresh_token
    user.last_login = datetime.utcnow()  # Oxirgi login vaqtini yangilash (opsional)
    db.commit()  # O'zgarishlarni saqlash

    return {
        "id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "access_token_expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token_expires_in": REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    }


@login_router.post("/refresh_token", response_model=Token)
def refresh_access_token(db: Session = Depends(database), refresh_token: str = ""):
    payload = decode_token(refresh_token, "refresh")
    username: Optional[str] = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    user = db.query(Users).filter(Users.username == username).first()
    if user is None or user.refresh_token != refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or invalid refresh token"
        )

    # Yangi access token yaratamiz
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.username}, expires_delta=access_token_expires, token_type="access"
    )

    # Access tokenni foydalanuvchi jadvaliga yozib qo'yamiz
    user.access_token = access_token
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# Dependencies
async def get_current_active_user(current_user: Users = Depends(get_current_user)) -> Users:
    return current_user
