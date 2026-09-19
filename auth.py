# Simple login for QueryPilot demo. Real app uses hashed passwords.
import secrets

# Demo users: name -> password and org.
USERS = {
    "amit": {"password": "amit123", "org_id": 1},
    "neha": {"password": "neha123", "org_id": 1},
    "ravi": {"password": "ravi123", "org_id": 2},
}

# Live tokens: token -> org_id.
TOKENS = {}


def login(name: str, password: str):
    """Check user and return (ok, message, token)."""
    user = USERS.get(name.strip().lower())
    if not user or user["password"] != password:
        return False, "wrong name or password", ""
    token = secrets.token_hex(16)
    TOKENS[token] = user["org_id"]
    return True, "welcome " + name, token


def get_org(token: str):
    """Get org_id from token, 0 means invalid."""
    return TOKENS.get(token, 0)