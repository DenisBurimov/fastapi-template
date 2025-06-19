from fastapi import APIRouter, Depends, Request
from app.templating import templates
from fastapi.responses import HTMLResponse
from app.dependencies import login_required


main_router = APIRouter()


@main_router.get("/", response_class=HTMLResponse)
@login_required
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "testing_index_variable": "Testing Index Page",
        },
    )


@main_router.get("/get_history", response_class=HTMLResponse)
async def get_history(request: Request):
    return templates.TemplateResponse("chat/history.html", {"request": request})


@main_router.post("/send_message", response_class=HTMLResponse)
async def send_message(request: Request):
    return templates.TemplateResponse("chat/history.html", {"request": request})
