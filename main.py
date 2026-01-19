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
