# Make SQL from question using Groq.
from langchain_groq import ChatGroq
import yaml
import re
from dotenv import load_dotenv

load_dotenv()

# Load rule-book.
with open("schema.yml") as f:
    SCHEMA = yaml.safe_load(f)

# Make Groq model.
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

def make_sql(question: str, org_id: int = 1):
    """Make SQL from question."""
    # Send schema + question to LLM.
    prompt = f"Tables: {SCHEMA}. Return only SELECT SQL, no markdown, no explanation for: {question}"
    out = llm.invoke(prompt)
    sql = out.content.strip()
    # Remove markdown cover if LLM adds it.
    sql = sql.replace("```sql", "").replace("```", "").strip()
    # Keep only SELECT part.
    up = sql.upper()
    if "SELECT" in up:
        sql = sql[up.find("SELECT"):].strip()
    # Cut extra explanation after ;
    if ";" in sql:
        sql = sql.split(";")[0] + ";"
    # Fix all leftover placeholders with safe defaults.
    sql = sql.replace(":org_id", str(org_id))
    sql = sql.replace("?", "1")
    sql = re.sub(r":\w+", "1", sql)
    # Force login org. LLM may write 1, server always wins.
    sql = re.sub(r"org_id\s*=\s*\d+", "org_id = " + str(org_id), sql)
    return sql.strip()

# Quick joint test.
if __name__ == "__main__":
    from guard import check_sql
    print(check_sql(make_sql("last 30 days city-wise orders?"), 1))