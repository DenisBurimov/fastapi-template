from fastapi import HTTPException, APIRouter, Depends
from sqlmodel import Session, select
from ldap3 import Server, Connection, ALL
from passlib.context import CryptContext
from app import models as m
from app.database import get_session
from config import Settings
from app.utils import create_access_token, get_current_user
import logging


CFG = Settings()
api_auth_router = APIRouter(prefix="/api/auth", tags=["auth"])
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")


def ldap_auth(username: str, password: str):
    server = Server(CFG.LDAP_SERVER, get_info=ALL)
    user_dn = CFG.LDAP_USER_FORMAT.format(username)
    conn = None

    try:
        conn = Connection(server, user=user_dn, password=password)
        if not conn.bind():
            return False
        conn.search(
            search_base=CFG.LDAP_BASE_DN,
            search_filter=CFG.LDAP_SEARCH_FILTER.format(username),
            attributes=["cn"],
        )
        if not conn.entries:
            raise HTTPException(status_code=403, detail="User not found in directory")
        return conn.entries[0]
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=403, detail="User not found in directory")
    finally:
        if conn:
            conn.unbind()


@api_auth_router.post("/login", response_model=m.UserToken)
async def api_login(login_data: m.UserLoginData, session: Session = Depends(get_session)):
    user = session.scalar(select(m.User).where(m.User.name == login_data.username))
    if not user:
        error_message = "User not found"
        logger.error(error_message)
        raise HTTPException(status_code=403, detail=error_message)
    if not user.verify_password(login_data.password):
        error_message = "Password mismatch"
        logger.error(error_message)
        raise HTTPException(status_code=403, detail=error_message)
    logger.info("User %s authenticated", login_data.username)
    access_token = create_access_token(dict(sub=login_data.username))
    return m.UserToken(
        access_token=access_token,
        token_type="Bearer",
    )


@api_auth_router.get("/profile", response_model=m.UserProfile)
async def api_profile(current_user: m.User = Depends(get_current_user)):
    return m.UserProfile(name=current_user.name, email=current_user.email, role=current_user.role)
