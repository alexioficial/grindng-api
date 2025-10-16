import os
from flask import Flask
from dotenv import load_dotenv

from db import create_indexes
from auth import auth_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    create_indexes()

    @app.get("/")
    def health():
        return {"status": 0, "msg": "ok", "data": {"service": "grindng-api"}}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)