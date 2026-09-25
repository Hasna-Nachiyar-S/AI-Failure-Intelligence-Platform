
import hashlib
import hmac
import os
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parent / "data" / "app.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SESSION_COOKIE = "afi_session"
SESSION_MAX_AGE = 60 * 60 * 24 * 7


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS sessions (
            token_hash TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            domain TEXT NOT NULL,
            prediction TEXT,
            probability REAL,
            input_json TEXT NOT NULL,
            result_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_analyses_user ON analyses(user_id);
        CREATE INDEX IF NOT EXISTS idx_analyses_created ON analyses(created_at);
        """)


def _now():
    return datetime.now(timezone.utc)


def _iso(dt):
    return dt.isoformat()


def _hash_password(password: str, salt: bytes) -> str:
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        310_000,
    )
    return f"pbkdf2_sha256$310000${salt.hex()}${digest.hex()}"


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    return _hash_password(password, salt)


def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = stored.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        salt = bytes.fromhex(salt_hex)
        expected = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(iterations),
        ).hex()
        return hmac.compare_digest(expected, digest_hex)
    except (ValueError, TypeError):
        return False


def create_user(full_name: str, email: str, password: str):
    now = _iso(_now())
    with _connect() as conn:
        try:
            cursor = conn.execute(
                """
                INSERT INTO users(full_name, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (full_name.strip(), email.strip().lower(), hash_password(password), now),
            )
            user_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("An account with this email already exists.")
    return get_user(user_id)


def authenticate(email: str, password: str):
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ? COLLATE NOCASE",
            (email.strip().lower(),),
        ).fetchone()
    if not row or not verify_password(password, row["password_hash"]):
        return None
    return dict(row)


def get_user(user_id: int):
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, full_name, email, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    return dict(row) if row else None


def create_session(user_id: int):
    raw_token = secrets.token_urlsafe(48)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    now = _now()
    expires = now.timestamp() + SESSION_MAX_AGE
    expires_dt = datetime.fromtimestamp(expires, tz=timezone.utc)

    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO sessions(token_hash, user_id, created_at, expires_at)
            VALUES (?, ?, ?, ?)
            """,
            (token_hash, user_id, _iso(now), _iso(expires_dt)),
        )
    return raw_token


def get_user_by_session(raw_token: Optional[str]):
    if not raw_token:
        return None
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT u.id, u.full_name, u.email, u.created_at
            FROM sessions s
            JOIN users u ON u.id = s.user_id
            WHERE s.token_hash = ? AND s.expires_at > ?
            """,
            (token_hash, _iso(_now())),
        ).fetchone()
    return dict(row) if row else None


def delete_session(raw_token: Optional[str]):
    if not raw_token:
        return
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    with _connect() as conn:
        conn.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))


def record_analysis(user_id: int, domain: str, prediction: Optional[str],
                    probability: Optional[float], input_json: str, result_json: str):
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO analyses(user_id, domain, prediction, probability,
                                  input_json, result_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, domain, prediction, probability, input_json, result_json, _iso(_now())),
        )


def get_dashboard(user_id: int):
    with _connect() as conn:
        total = conn.execute(
            "SELECT COUNT(*) AS n FROM analyses WHERE user_id = ?", (user_id,)
        ).fetchone()["n"]

        domains = conn.execute(
            """
            SELECT domain, COUNT(*) AS count
            FROM analyses
            WHERE user_id = ?
            GROUP BY domain
            ORDER BY count DESC, domain
            """,
            (user_id,),
        ).fetchall()

        recent = conn.execute(
            """
            SELECT id, domain, prediction, probability, created_at
            FROM analyses
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 10
            """,
            (user_id,),
        ).fetchall()

        avg = conn.execute(
            """
            SELECT AVG(probability) AS average_probability
            FROM analyses
            WHERE user_id = ? AND probability IS NOT NULL
            """,
            (user_id,),
        ).fetchone()["average_probability"]

    return {
        "total_analyses": total,
        "domain_breakdown": [dict(row) for row in domains],
        "recent_analyses": [dict(row) for row in recent],
        "average_probability": avg,
    }


def get_history(user_id: int, limit: int = 50):
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, domain, prediction, probability, input_json, result_json, created_at
            FROM analyses
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, min(max(limit, 1), 100)),
        ).fetchall()
    return [dict(row) for row in rows]


init_db()
