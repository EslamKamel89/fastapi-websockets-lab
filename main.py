from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

BASEDIR = Path(__file__).resolve().parent
print("BASEDIR", BASEDIR)
HTML_FILE = BASEDIR / "templates" / "index.html"
print("HTML_FILE", HTML_FILE)

app = FastAPI()


@app.get("/")
async def get():
    return HTMLResponse(HTML_FILE.read_text(encoding="utf-8"))
