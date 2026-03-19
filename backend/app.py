import os
import json
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS


from services.body_shape import detect_body_shape
from services.recommender import get_dress_recommendations
from services.skin_tone_model import detect_skin_tone
from services.chatbot import get_fashion_chatbot_response

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # backend/
PROJECT_DIR = os.path.dirname(BASE_DIR)                        # project root
FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")
FRONTEND_IMAGES_DIR = os.path.join(FRONTEND_DIR, "images")

UPLOAD_FOLDER = os.path.join(PROJECT_DIR, "uploads")
DATABASE_DIR = os.path.join(BASE_DIR, "database")
USERS_FILE = os.path.join(DATABASE_DIR, "users.json")
COLOR_RULES_FILE = os.path.join(PROJECT_DIR, "data", "color_rules.json")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATABASE_DIR, exist_ok=True)


def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


@app.route("/")
def home():
    return "Backend Running Successfully"


@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json() or {}
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        users = load_users()

        for user in users:
            if user["username"].lower() == username.lower():
                return jsonify({"error": "Username already exists"}), 400

        users.append({
            "username": username,
            "password": password
        })
        save_users(users)

        return jsonify({"message": "Signup successful"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json() or {}
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        users = load_users()

        for user in users:
            if user["username"] == username and user["password"] == password:
                return jsonify({
                    "message": "Login successful",
                    "username": username
                }), 200

        return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/upload/body", methods=["POST"])
def upload_body():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        if "category" not in request.form:
            return jsonify({"error": "No category selected"}), 400

        file = request.files["image"]
        category = request.form["category"].strip()

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        print("Saved body image path:", filepath)
        print("Selected category:", category)

        body_result = detect_body_shape(filepath)
        print("Body result:", body_result)

        if "error" in body_result:
            return jsonify(body_result), 400

        body_shape = body_result.get("body_shape", "unknown")
        confidence = body_result.get("confidence", 0)
        message = body_result.get("message", "")

        if body_shape in ["unknown", "uncertain", "error"]:
            return jsonify({
                "body_shape": body_shape,
                "confidence": confidence,
                "message": message,
                "category": category,
                "recommendations": []
            }), 200

        recommendation_result = get_dress_recommendations(body_shape, category)
        print("Recommendation result:", recommendation_result)

        if "error" in recommendation_result:
            return jsonify(recommendation_result), 400

        return jsonify({
            "body_shape": body_shape,
            "confidence": confidence,
            "message": message,
            "category": category,
            "recommendations": recommendation_result.get("recommendations", [])
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/upload/skin", methods=["POST"])
def upload_skin():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        print("Saved skin image path:", filepath)

        skin_result = detect_skin_tone(filepath)
        print("Skin result:", skin_result)

        if "error" in skin_result:
            return jsonify(skin_result), 400

        with open(COLOR_RULES_FILE, "r", encoding="utf-8") as f:
            color_rules = json.load(f)

        skin_tone = skin_result.get("skin_tone", "").strip().lower()
        confidence = skin_result.get("confidence", 0)

        # Since Roboflow skin tone model usually predicts only tone,
        # keep undertone as default for now
        undertone = "Neutral"

        suggested_colors = color_rules.get(skin_tone, {}).get(undertone, [])

        return jsonify({
            "skin_tone": skin_tone,
            "confidence": confidence,
            "undertone": undertone,
            "suggested_colors": suggested_colors
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/get_colors", methods=["GET"])
def get_colors():
    try:
        tone = request.args.get("tone", "").strip().lower()
        undertone = request.args.get("undertone", "").strip()

        with open(COLOR_RULES_FILE, "r", encoding="utf-8") as f:
            color_rules = json.load(f)

        colors = color_rules.get(tone, {}).get(undertone, [])
        return jsonify({"colors": colors}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"reply": "Please ask a fashion-related question."}), 200

        reply = get_fashion_chatbot_response(message)
        return jsonify({"reply": reply}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/images/<path:filename>")
def serve_images(filename):
    return send_from_directory(FRONTEND_IMAGES_DIR, filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)