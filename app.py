# API for QueryPilot.
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import redis
from graph import run_q
from clarify import check_question
from auth import login as user_login, get_org
from db import run_sql

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


@app.get("/login")
def login(name: str, password: str):
    """Give token for valid user."""
    ok, message, token = user_login(name, password)
    return {"ok": ok, "message": message, "token": token}

# Make cache link. Uses Render Redis if set, else local.
REDIS_URL = os.getenv("REDIS_URL")
try:
    if REDIS_URL:
        cache = redis.from_url(REDIS_URL, decode_responses=True)
    else:
        cache = redis.Redis(host="localhost", port=6379, decode_responses=True)
    cache.ping()
except Exception:
    cache = None

@app.get("/query")
def query(q: str, token: str = "", approved: str = ""):
    """Run question to SQL for logged in org."""
    # 0. Token gives org, chat never gives org.
    org = get_org(token)
    if org == 0:
        return {"ok": False, "message": "login first", "sql": ""}
    yes = approved == "yes"
    # 1. Check cache first. Key has org so orgs never share.
    key = f"{org}:{q}:{approved}"
    if cache:
        old = cache.get(key)
        if old:
            return {"cached": True, "result": old}
    # 2. Run graph if not found.
    out = run_q(q, org, yes)
    # 3. Run safe SQL and attach rows.
    if out.get("ok"):
        cols, rows = run_sql(out.get("sql", ""))
        out["cols"] = cols
        out["rows"] = rows
    # 4. Save for next time.
    if cache:
        cache.set(key, str(out), ex=300)
    return out

@app.get("/audit")
def audit():
    """Show past queries."""
    try:
        with open("audit.log") as f:
            return {"log": f.read().splitlines()[-20:]}
    except FileNotFoundError:
        return {"log": []}
