from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

from db import create_indexes
from auth import auth_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(auth_bp)
    create_indexes()

    @app.get("/")
    def health():
        return {"status": 0, "msg": "ok", "data": {"service": "grindng-api"}}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8100, debug=True)
