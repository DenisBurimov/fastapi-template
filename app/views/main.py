from fastapi import APIRouter, Depends, Request
from app.templating import templates
from fastapi.responses import HTMLResponse


main_router = APIRouter()


@main_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "testing_index_variable": "Testing Index Page",
        },
    )
