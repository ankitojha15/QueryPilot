# Simple eval for QueryPilot. Checks 5 cases.
from clarify import check_question
from guard import check_sql
from graph import run_q

score = 0
total = 5

# 1. Clear question goes ok.
s, _, _ = check_question("last 30 days city-wise orders?")
if s == "ok":
    score += 1
    print("1 pass: clear question")

# 2. Unclear question needs help.
s, _, _ = check_question("where are my orders?")
if s == "need_clarification":
    score += 1
    print("2 pass: unclear caught")

# 3. Good SQL passes guard.
ok, _, _ = check_sql("SELECT id FROM customers WHERE org_id=1", 1)
if ok:
    score += 1
    print("3 pass: good SQL")

# 4. Bad SQL blocked.
ok, _, _ = check_sql("DELETE FROM customers", 1)
if not ok:
    score += 1
    print("4 pass: bad SQL blocked")

# 5. Full flow works.
out = run_q("last 30 days city-wise orders?")
if out.get("ok"):
    score += 1
    print("5 pass: full flow")

print(f"Score: {score}/{total}")
if score * 100 // total >= 80:
    print("Eval 80 pass")
else:
    print("Eval 80 fail")