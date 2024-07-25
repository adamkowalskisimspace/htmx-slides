from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


async def current_count(request: Request) -> int:
    form_data = await request.form()
    count = form_data["count"]
    assert isinstance(count, str)
    return int(count)


def counter_template(request: Request, count: int):
    return templates.TemplateResponse(
        request=request,
        name=f"/counter.html",
        context={"count": count},
    )


@router.post("/counter/decrement", response_class=HTMLResponse)
async def decrement_counter(request: Request):
    count = await current_count(request)
    return counter_template(request, count - 1)


@router.post("/counter/increment", response_class=HTMLResponse)
async def increment_counter(request: Request):
    count = await current_count(request)
    return counter_template(request, count + 1)


@router.post("/counter/reset", response_class=HTMLResponse)
async def reset_counter(request: Request):
    return counter_template(request, 0)
