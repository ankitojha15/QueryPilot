# QueryPilot — Natural Language to SQL Agent

Ask analytics questions in plain English, get answers with SQL + charts. Unsafe queries are blocked.

> Example: "Last 30 days city-wise orders?" → Safe SQL → Results + Chart

## Features
- Natural language to SQL using LLM
- Only SELECT queries allowed (DROP / DELETE / UPDATE auto-blocked)
- `org_id` filter compulsory for multi-tenant safety
- `LIMIT 200` auto-added to protect DB
- Self-fix: if SQL fails, agent retries with DB error (max 2 times)
- Redis cache for repeated questions
- APIs: `/query`, `/audit`

## Tech Stack
FastAPI,Langchain , LangGraph, Postgres, Redis, SQLAlchemy, Groq, Docker