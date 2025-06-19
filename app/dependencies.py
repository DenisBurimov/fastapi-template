from fastapi import Request, HTTPException
from starlette import status
from functools import wraps


def login_required(route):
    @wraps(route)
    async def wrapper(request: Request, *args, **kwargs):
        if "user_id" not in request.session:
            raise HTTPException(status_code=status.HTTP_302_FOUND, headers={"Location": "/auth/login"})
        return await route(request, *args, **kwargs)

    return wrapper
