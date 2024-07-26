import json
from fastapi import APIRouter, WebSocket
from jinja2 import Environment, FileSystemLoader

router = APIRouter()

env = Environment(loader=FileSystemLoader("templates"))


@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        json_data = json.loads(data)
        message = json_data["message"]
        template = env.get_template("chat.html")
        html = template.render(message=message)
        await websocket.send_text(html)
