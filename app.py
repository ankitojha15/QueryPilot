# API for QueryPilot.
from fastapi import FastAPI
from graph import run_q

# Make API.
app = FastAPI(title="QueryPilot")

@app.get("/query")
def query(q: str):
    """Run question to SQL."""
    return run_q(q)

@app.get("/audit")
def audit():
    """Show past queries."""
    with open("audit.log") as f:
        return {"log": f.read().splitlines()[-20:]}