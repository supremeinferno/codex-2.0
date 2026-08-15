import sqlite3
import hashlib
from datetime import datetime


DB_PATH = "users.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Login activity
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ==========================================================
# REGISTER
# ==========================================================

def register_user(email, password):

    email = email.strip().lower()

    if not email or not password:
        return False, "Email and password are required."

    password_hash = hash_password(password)

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (
                email,
                password_hash
            )
            VALUES (?, ?)
            """,
            (
                email,
                password_hash,
            )
        )

        conn.commit()
        conn.close()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "An account with this email already exists."


# ==========================================================
# LOGIN
# ==========================================================

def login_user(email, password):

    email = email.strip().lower()

    password_hash = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, email
        FROM users
        WHERE email = ?
        AND password_hash = ?
        """,
        (
            email,
            password_hash,
        )
    )

    user = cursor.fetchone()

    if not user:

        conn.close()

        return False, "Invalid email or password."

    user_id = user[0]
    user_email = user[1]

    # Record successful login
    cursor.execute(
        """
        INSERT INTO login_activity (
            user_id,
            email
        )
        VALUES (?, ?)
        """,
        (
            user_id,
            user_email,
        )
    )

    conn.commit()
    conn.close()

    return True, {
        "id": user_id,
        "email": user_email,
    }


# ==========================================================
# USER STATISTICS
# ==========================================================

def get_total_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_logins():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM login_activity"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_login_activity():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            user_id,
            email,
            login_time
        FROM login_activity
        ORDER BY login_time DESC
        """
    )

    activity = cursor.fetchall()

    conn.close()

    return activity


def get_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            email,
            created_at
        FROM users
        ORDER BY created_at DESC
        """
    )

    users = cursor.fetchall()

    conn.close()

    return users


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

init_db()