# QueryPilot — Natural Language to SQL Agent

Ask in English, get safe SQL + results. Unsafe queries blocked.

> Example: "Last 30 days city-wise orders?" -> Safe SQL -> Results

## Features
- Natural language to SQL using Groq
- Only SELECT allowed (DROP / DELETE / UPDATE auto-blocked)
- `org_id` filter compulsory, `LIMIT 200` auto-added
- PII `email` blocked, audit in `audit.log`
- Clarify unclear questions (city/state, 7/30/90 days)
- Redis cache for repeat questions
- APIs: `/query`, `/audit`
- Eval 5/5 pass

## Run
docker compose up -d
docker exec -i querypilot-db-1 psql -U pilot -d pilot < seed.sql
./qpenv/bin/uvicorn app:app --port 8000
./qpenv/bin/streamlit run ui.py --server.port 8501
./qpenv/bin/python eval.py


## Tech Stack
FastAPI, LangChain-Core, LangChain-Groq, LangGraph, Postgres, Redis, sqlglot, Docker