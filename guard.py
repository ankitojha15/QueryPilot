# Simple safety check for SQL. Only SELECT is allowed.
import yaml
import sqlglot

# Load allowed rules from schema file.
with open("schema.yml") as f:
    SCHEMA = yaml.safe_load(f)

BLOCKED_WORDS = ["drop", "delete", "update", "insert", "alter", "truncate"]
PII_COLUMNS = ["email"]


def check_sql(sql: str, org_id: int):
    """Check SQL and return (is_ok, message, safe_sql)."""
    low = sql.lower().strip()

    # 1. Only SELECT query is allowed.
    if not low.startswith("select"):
        return False, "Only SELECT is allowed", ""

    # 2. Block dangerous commands.
    for word in BLOCKED_WORDS:
        if word in low:
            return False, f"Blocked word found: {word}", ""

    # 3. Block PII columns.
    for col in PII_COLUMNS:
        if col in low:
            return False, f"PII column blocked: {col}", ""

    # 4. org_id filter is compulsory.
    if "org_id" not in low:
        return False, "org_id filter is missing", ""

    # 5. Add LIMIT 200 if missing.
    try:
        tree = sqlglot.parse_one(sql)
        if tree.args.get("limit") is None:
            sql = sql.rstrip().rstrip(";") + " LIMIT 200"
    except Exception:
        # If parse fails, keep original SQL.
        pass

    # 6. Save to audit log.
    with open("audit.log", "a") as log:
        log.write(f"org={org_id} | {sql}\n")

    return True, "ok", sql