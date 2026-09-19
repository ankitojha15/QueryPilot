# Check unclear question for Streamlit buttons.
def check_question(text: str):
    """Return status, message, options."""
    low = text.lower().strip()

    # Case 0: destructive request is blocked.
    for word in ["delete", "drop", "update", "remove", "insert", "alter", "truncate"]:
        if word in low:
            return ("blocked", "I only run safe SELECT queries. Delete / update is not allowed.", [])

    # Case 1: location missing in order question.
    if "where" in low and "order" in low:
        if "city" not in low and "state" not in low:
            return ("need_clarification", "Do you want city-wise or state-wise result?", ["city-wise", "state-wise"])

    # Case 2: time range missing in sales question.
    if "sales" in low or "order" in low:
        if "day" not in low and "month" not in low and "year" not in low:
            return ("need_clarification", "For which time range?", ["last 7 days", "last 30 days", "last 90 days"])

    # Case 3: sensitive request needs approval.
    if "email" in low or "all data" in low or "full" in low:
        return ("need_approval", "This looks sensitive. Should I run it?", ["yes-run", "cancel"])

    # Case 4: clear question.
    return ("ok", "clear question", [])