from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select
from passlib.context import CryptContext
from fastapi.responses import HTMLResponse, RedirectResponse
from app.templating import templates
from app import models as m
from app.database import get_session
from config import Settings
import logging


CFG = Settings()
auth_router = APIRouter(prefix="/auth")
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")


@auth_router.api_route("/login", methods=["GET", "POST"])
async def login(
    request: Request,
    # login_data: m.UserLoginData,
    session: Session = Depends(get_session),
):
    if request.method == "POST":
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        user: m.User = session.scalar(select(m.User).where(m.User.name == username))
        if not user:
            error_message = "User not found"
            logger.error(error_message)
            return RedirectResponse(f"/auth/login?error_message={error_message}")
        if not user.verify_password(password):
            error_message = "Password mismatch"
            logger.error(error_message)
            return RedirectResponse(f"/auth/login?error_message={error_message}")

        request.session["user_id"] = user.id
        logger.info("User %s authenticated", username)
        return RedirectResponse("/", status_code=302)

    error_message = request.query_params.get("error_message")
    return templates.TemplateResponse("auth/login.html", {"request": request, "error_message": error_message})


@auth_router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/auth/login", status_code=302)
