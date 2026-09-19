# API for QueryPilot.
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import redis
from graph import run_q
from clarify import check_question

# Make API.
app = FastAPI(title="QueryPilot")

# Serve static UI files.
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    """Show main UI page."""
    return FileResponse("static/index.html")


@app.get("/clarify")
def clarify(q: str):
    """Check unclear question."""
    status, message, options = check_question(q)
    return {"status": status, "message": message, "options": options}

# Make cache link.
try:
    cache = redis.Redis(host="localhost", port=6379, decode_responses=True)
    cache.ping()
except Exception:
    cache = None

@app.get("/query")
def query(q: str):
    """Run question to SQL."""
    # 1. Check cache first.
    if cache:
        old = cache.get(q)
        if old:
            return {"cached": True, "result": old}
    # 2. Run graph if not found.
    out = run_q(q)
    # 3. Save for next time.
    if cache:
        cache.set(q, str(out), ex=300)
    return out

@app.get("/audit")
def audit():
    """Show past queries."""
    with open("audit.log") as f:
        return {"log": f.read().splitlines()[-20:]}