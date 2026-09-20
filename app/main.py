from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from app.routers import calculator, history

PROJECT_ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculator.router)
app.include_router(history.router)


@app.get("/", response_class=HTMLResponse)
def read_index():
    return FileResponse(PROJECT_ROOT / "index.html")


@app.get("/styles.css")
def read_css():
    return FileResponse(PROJECT_ROOT / "styles.css")


@app.get("/index.js")
def read_js():
    return FileResponse(PROJECT_ROOT / "index.js")
