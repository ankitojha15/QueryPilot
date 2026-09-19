# Join agent and guard with graph.
from typing import TypedDict
from langgraph.graph import StateGraph, END
from agent import make_sql
from guard import check_sql

# Data that moves in graph.
class State(TypedDict):
    question: str
    org_id: int
    sql: str
    ok: bool

# Step 1: make SQL.
def step_make(s: State):
    return {"sql": make_sql(s["question"], s.get("org_id", 1))}

# Step 2: check SQL.
def step_check(s: State):
    ok, _, safe = check_sql(s["sql"], s.get("org_id", 1))
    return {"sql": safe, "ok": ok}

# Build graph.
g = StateGraph(State)
g.add_node("make", step_make)
g.add_node("check", step_check)
g.set_entry_point("make")
g.add_edge("make", "check")
g.add_edge("check", END)
app = g.compile()

def run_q(question: str, org_id: int = 1):
    """Run full flow."""
    return app.invoke({"question": question, "org_id": org_id})