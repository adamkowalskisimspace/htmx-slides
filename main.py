from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from slides import counter

app = FastAPI()

app.include_router(counter.router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=RedirectResponse)
def read_root():
    return RedirectResponse(url="/slides/0")


@app.get("/slides/{slide}", response_class=HTMLResponse)
def read_slide(slide: int, request: Request):
    next_slide_exists = Path(f"templates/slides/{slide + 1}.html").exists()
    print(
        {
            "current": slide,
            "previous": slide - 1 if slide != 0 else None,
            "next": slide + 1 if next_slide_exists else None,
        }
    )
    return templates.TemplateResponse(
        request=request,
        name=f"/slides/{slide}.html",
        context={
            "current": slide,
            "previous": slide - 1 if slide != 0 else None,
            "next": slide + 1 if next_slide_exists else None,
        },
    )
