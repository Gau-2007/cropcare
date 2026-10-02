import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "cropcare.db"


def _conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def get_disease_info(class_name):
    with _conn() as c:
        row = c.execute("SELECT * FROM diseases WHERE class_name = ?",
                        (class_name,)).fetchone()
    return dict(row) if row else None


def save_prediction(image_path, predicted_class, confidence):
    with _conn() as c:
        c.execute("INSERT INTO predictions (image_path, predicted_class, confidence) VALUES (?, ?, ?)",
                  (image_path, predicted_class, confidence))


def get_history(limit=5):
    with _conn() as c:
        rows = c.execute(
            "SELECT p.id, p.confidence, p.created_at, p.predicted_class, d.display_name "
            "FROM predictions p LEFT JOIN diseases d ON d.class_name = p.predicted_class "
            "ORDER BY p.id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]