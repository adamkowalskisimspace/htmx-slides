import asyncio
from typing import AsyncGenerator
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


def encode_html(template_response: HTMLResponse) -> str:
    html = template_response.body.decode()
    return html.replace(chr(10), "").replace(chr(13), "")


async def progress_meter(request: Request) -> AsyncGenerator[str, None]:
    for progress in range(11):
        template_response = templates.TemplateResponse(
            request=request,
            name=f"/progress_meter.html",
            context={"progress": progress * 10},
        )
        html = encode_html(template_response)
        yield f"data: {html}\n\n"
        await asyncio.sleep(1)


@router.get("/progress-meter", response_class=StreamingResponse)
async def get_progress_meter(request: Request):
    return StreamingResponse(progress_meter(request), media_type="text/event-stream")
