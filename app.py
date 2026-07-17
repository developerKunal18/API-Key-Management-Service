from flask import Flask, request, jsonify
from models import db, ApiKey
import uuid

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///apikeys.db"

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------- Generate API Key ----------
@app.route("/generate", methods=["POST"])
def generate():

    key = str(uuid.uuid4())

    api_key = ApiKey(key=key)

    db.session.add(api_key)
    db.session.commit()

    return jsonify({
        "api_key": key
    })


# ---------- Validate API Key ----------
@app.route("/validate")
def validate():

    key = request.headers.get("X-API-Key")

    api_key = ApiKey.query.filter_by(
        key=key,
        active=True
    ).first()

    if not api_key:

        return jsonify({
            "message": "Invalid API Key"
        }), 401

    return jsonify({
        "message": "Valid API Key"
    })


# ---------- Revoke API Key ----------
@app.route("/revoke", methods=["POST"])
def revoke():

    data = request.get_json()

    api_key = ApiKey.query.filter_by(
        key=data["key"]
    ).first()

    if not api_key:

        return jsonify({
            "message": "Key not found"
        }), 404

    api_key.active = False

    db.session.commit()

    return jsonify({
        "message": "API Key Revoked"
    })


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(debug=True)
