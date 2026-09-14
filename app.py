# API for QueryPilot.
from fastapi import FastAPI
import redis
from graph import run_q

# Make API.
app = FastAPI(title="QueryPilot")

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