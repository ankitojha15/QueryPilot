# Run safe SQL on Postgres and give rows.
import os
from sqlalchemy import create_engine, text

# Render gives DATABASE_URL, local uses pilot db.
DB_URL = os.getenv("DATABASE_URL", "postgresql://pilot:pilot@localhost:5432/pilot")
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)

# One engine for all queries.
engine = create_engine(DB_URL, pool_pre_ping=True)


def run_sql(sql: str):
    """Run SELECT and return (columns, rows). Empty on failure."""
    try:
        with engine.connect() as conn:
            out = conn.execute(text(sql))
            cols = list(out.keys())
            rows = [list(r) for r in out.fetchmany(200)]
            return cols, rows
    except Exception:
        return [], []