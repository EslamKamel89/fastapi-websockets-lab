from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

BASEDIR = Path(__file__).resolve().parent
HEAD_FILE = BASEDIR / "templates" / "partials" / "head.html"
HTML_FILE = BASEDIR / "templates" / "index.html"
FOOTER_FILE = BASEDIR / "templates" / "partials" / "footer.html"

app = FastAPI()


@app.get("/")
async def get():
    content = f"""
    {HEAD_FILE.read_text(encoding='utf-8')}
    {HTML_FILE.read_text(encoding='utf-8')}
    {FOOTER_FILE.read_text(encoding='utf-8')}
    """
    return HTMLResponse(content)


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Message is {data}", websocket)
            await manager.broadcast_message(f"Client {client_id} says {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast_message(f"Client {client_id} has left the chat")
