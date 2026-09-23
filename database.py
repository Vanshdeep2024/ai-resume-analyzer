import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE_NAME = "resume_analyzer.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Resume analysis history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resume_name TEXT,
            target_role TEXT,
            overall_score REAL,
            role_score REAL,
            ats_score REAL,
            skills_count INTEGER,
            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def create_user(username, email, password):

    try:

        conn = get_connection()
        cursor = conn.cursor()

        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users (
                username,
                email,
                password
            )
            VALUES (?, ?, ?)
        """, (
            username,
            email,
            hashed_password
        ))

        conn.commit()

        user_id = cursor.lastrowid

        conn.close()

        return {
            "success": True,
            "user_id": user_id
        }

    except sqlite3.IntegrityError as e:

        if "username" in str(e).lower():

            message = "Username already exists."

        elif "email" in str(e).lower():

            message = "Email already exists."

        else:

            message = "Username or email already exists."

        return {
            "success": False,
            "message": message
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


def authenticate_user(login_value, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ?
           OR email = ?
    """, (
        login_value,
        login_value
    ))

    user = cursor.fetchone()

    conn.close()

    if user is None:

        return None

    if check_password_hash(
        user["password"],
        password
    ):

        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }

    return None


def save_analysis(
    user_id,
    resume_name,
    target_role,
    overall_score,
    role_score,
    ats_score,
    skills_count
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analysis_history (
            user_id,
            resume_name,
            target_role,
            overall_score,
            role_score,
            ats_score,
            skills_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        resume_name,
        target_role,
        overall_score,
        role_score,
        ats_score,
        skills_count
    ))

    conn.commit()
    conn.close()

    return True


def get_user_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            resume_name,
            target_role,
            overall_score,
            role_score,
            ats_score,
            skills_count,
            analysis_date
        FROM analysis_history
        WHERE user_id = ?
        ORDER BY analysis_date DESC
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    history = []

    for row in rows:

        history.append({
            "id": row["id"],
            "resume_name": row["resume_name"],
            "target_role": row["target_role"],
            "overall_score": row["overall_score"],
            "role_score": row["role_score"],
            "ats_score": row["ats_score"],
            "skills_count": row["skills_count"],
            "analysis_date": row["analysis_date"]
        })

    return history


# Create database and tables automatically
initialize_database()