import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI, Query  ##Query is using with history function
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter
from fastapi.responses import HTMLResponse, FileResponse ## Both using for Serve Frontend Web Files

from calculator import expand_percent

HISTORY_MAX = 1000
# HISTORY (in-memory for now)
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.post("/calculate")
def calculate(expr: str):
    try:
        code = expand_percent(expr)
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}

        # TODO: Add history
        history.appendleft({
            "expr": expr,
            "result": str(result),
            "timestamp": datetime.now().isoformat()
        })

        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}

## TODO GET /hisory
@app.get("/history")
def get_history(limit: int = Query(50, ge=1, le=100)):
    """
    Returns the most recent calculation history items up to the limit.
    """
    return list(history)[:limit]

## TODO DELETE /history
@app.delete("/history")
def clear_history():
    """
    Clears all saved history entries.
    """
    history.clear()
    return {"ok": True, "message": "History cleared successfully"}


# ---------- Serve Frontend Files Directly at Root (No /static prefix) ----------

@app.get("/", response_class=HTMLResponse)
def read_index():
    return FileResponse("index.html")


@app.get("/styles.css")
def read_css():
    return FileResponse("styles.css")


@app.get("/index.js")
def read_js():
    return FileResponse("index.js")