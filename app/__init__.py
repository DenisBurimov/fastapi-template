from fastapi import FastAPI, Request
from pathlib import Path

from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount

from config import Settings
from .database import get_session
from sqlmodel import Session
from typing import Callable
import logging


CFG = Settings()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")


def create_app(session_dependency: Callable[[], Session] = get_session) -> FastAPI:
    load_dotenv()
    app = FastAPI()
    app.add_middleware(SessionMiddleware, secret_key=CFG.SECRET_KEY)
    app.dependency_overrides[get_session] = session_dependency
    base_dir = Path(__file__).resolve().parent
    static_dir = base_dir / "static"

    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    from .routers import api_auth_router
    from .views import main_router, auth_router

    app.include_router(api_auth_router)
    app.include_router(main_router)
    app.include_router(auth_router)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        print(f"ValidationError: {exc}")
        logger.error("ValidationError %s", exc)
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.get("/health")
    def health():
        routes = []
        for route in app.routes:
            if isinstance(route, Mount):
                continue
            route_data = dict(
                url=route.path,
                methods=route.methods,
                name=route.name,
            )
            routes.append(route_data)
            logger.info(route_data)
        logger.info("Routes found: %s", len(routes))
        return {"status": "OK", "statusCode": 200, "routes": routes}

    return app


app = create_app()
