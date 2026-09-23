from flask import Flask, request, jsonify

from database import (
    create_user,
    authenticate_user,
    save_analysis,
    get_user_history
)


app = Flask(__name__)


# ============================================================
# REGISTER
# ============================================================

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No data received."
        }), 400

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not username or not email or not password:

        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    result = create_user(
        username,
        email,
        password
    )

    if result["success"]:

        return jsonify({
            "success": True,
            "message": "Account created successfully."
        })

    return jsonify(result), 400


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No data received."
        }), 400

    login_value = data.get("login", "").strip()
    password = data.get("password", "")

    if not login_value or not password:

        return jsonify({
            "success": False,
            "message": "Username/email and password are required."
        }), 400

    user = authenticate_user(
        login_value,
        password
    )

    if user:

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "user": user
        })

    return jsonify({
        "success": False,
        "message": "Invalid username/email or password."
    }), 401


# ============================================================
# SAVE ANALYSIS
# ============================================================

@app.route("/save-analysis", methods=["POST"])
def save_analysis_route():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No data received."
        }), 400

    required_fields = [
        "user_id",
        "resume_name",
        "target_role",
        "overall_score",
        "role_score",
        "ats_score",
        "skills_count"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "success": False,
                "message": f"Missing field: {field}"
            }), 400

    try:

        save_analysis(
            user_id=data["user_id"],
            resume_name=data["resume_name"],
            target_role=data["target_role"],
            overall_score=data["overall_score"],
            role_score=data["role_score"],
            ats_score=data["ats_score"],
            skills_count=data["skills_count"]
        )

        return jsonify({
            "success": True,
            "message": "Analysis saved successfully."
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ============================================================
# HISTORY
# ============================================================

@app.route("/history/<int:user_id>", methods=["GET"])
def history(user_id):

    try:

        user_history = get_user_history(user_id)

        return jsonify({
            "success": True,
            "history": user_history
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ============================================================
# TEST ROUTE
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "AI Resume Analyzer Flask Backend is running."
    })


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )