from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

from db import users_col
from utils.jwt_utils import generate_jwt, verify_jwt

auth_bp = Blueprint("auth", __name__)


def ok(data=None, msg="ok"):
    return jsonify({"status": 0, "msg": msg, "data": data or {}}), 200


def err(msg="error", data=None):
    # status 1 siempre representa error
    return jsonify({"status": 1, "msg": msg, "data": data}), 200


@auth_bp.post("/register")
def register():
    body = request.get_json(silent=True) or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    if not email or not password:
        return err("Email y contraseña son requeridos")

    if users_col().find_one({"email": email}):
        return err("El email ya está registrado")

    hashed = generate_password_hash(password)
    user = {"email": email, "password": hashed}
    res = users_col().insert_one(user)
    user_id = str(res.inserted_id)
    return ok({"id": user_id})


@auth_bp.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    if not email or not password:
        return err("Email y contraseña son requeridos")

    user = users_col().find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return err("Credenciales inválidas")

    token = generate_jwt({"sub": str(user["_id"]), "email": email})
    return ok({"token": token})


def _get_bearer_token() -> str | None:
    auth = request.headers.get("Authorization") or ""
    if auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    return None


@auth_bp.get("/me")
def me():
    token = _get_bearer_token()
    if not token:
        return err("No autenticado")
    payload = verify_jwt(token)
    if not payload:
        return err("Token inválido o expirado")
    # datos minimos del perfil
    return ok({"email": payload.get("email"), "id": payload.get("sub")})
