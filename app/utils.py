from datetime import datetime, timedelta, UTC
from jose import jwt
from sqlmodel import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app import models as m
from app.database import get_session
from config import Settings
import logging


CFG = Settings()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=CFG.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, CFG.JWT_SECRET_KEY, algorithm=CFG.JWT_ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(get_session)):
    try:
        payload = jwt.decode(token, CFG.JWT_SECRET_KEY, algorithms=[CFG.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            logger.error("Invalid token")
            raise credentials_exception
    except Exception as e:
        logger.error(e)
        raise credentials_exception

    user = session.scalar(select(m.User).where(m.User.name == username))
    if not user:
        logger.error(f"{username} not found")
        raise credentials_exception

    logger.info(f"User {username} verified")
    return user
