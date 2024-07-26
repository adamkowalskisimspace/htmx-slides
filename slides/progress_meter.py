import asyncio
from typing import AsyncGenerator
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from jinja2 import Environment, FileSystemLoader

router = APIRouter()

env = Environment(loader=FileSystemLoader("templates"))


async def progress_meter(request: Request) -> AsyncGenerator[str, None]:
    for progress in range(11):
        template = env.get_template("progress_meter.html")
        html = template.render(progress=progress * 10)
        encoded_html = html.replace(chr(10), "").replace(chr(13), "")
        yield f"data: {encoded_html}\n\n"
        await asyncio.sleep(1)


@router.get("/progress-meter", response_class=StreamingResponse)
async def get_progress_meter(request: Request):
    return StreamingResponse(progress_meter(request), media_type="text/event-stream")
