from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/slides/{slide}", response_class=HTMLResponse)
def read_slide(slide: int, request: Request):
    next_slide_exists = Path(f"templates/slides/{slide + 1}.html").exists()
    return templates.TemplateResponse(
        request=request,
        name=f"/slides/{slide}.html",
        context={
            "current": slide,
            "previous": slide - 1 if slide != 0 else None,
            "next": slide + 1 if next_slide_exists else None,
        },
    )
