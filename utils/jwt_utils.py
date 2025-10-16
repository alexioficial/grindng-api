import os
import datetime as dt
import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_EXPIRES_HOURS = int(os.getenv("JWT_EXPIRES_HOURS", "24"))


def generate_jwt(payload: dict) -> str:
    exp = dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=JWT_EXPIRES_HOURS)
    to_encode = {**payload, "exp": exp}
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")


def verify_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None
