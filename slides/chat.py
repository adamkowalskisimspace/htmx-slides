import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jinja2 import Environment, FileSystemLoader

router = APIRouter()

env = Environment(loader=FileSystemLoader("templates"))


connections: list[WebSocket] = []


@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            message = json_data["message"]
            template = env.get_template("chat.html")
            html = template.render(message=message)
            for connection in connections:
                await connection.send_text(html)
    except WebSocketDisconnect:
        connections.remove(websocket)
