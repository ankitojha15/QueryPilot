# Make SQL from question using Groq.
from langchain_groq import ChatGroq
import yaml
from dotenv import load_dotenv

load_dotenv()

# Load rule-book.
with open("schema.yml") as f:
    SCHEMA = yaml.safe_load(f)

# Make Groq model.
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

def make_sql(question: str):
    """Make SQL from question."""
    # Send schema + question to LLM.
    prompt = f"Tables: {SCHEMA}. Make only SELECT SQL for: {question}"
    out = llm.invoke(prompt)
    return out.content.strip()

# Quick joint test.
from guard import check_sql
print(check_sql(make_sql("last 30 days city-wise orders?"), 1))