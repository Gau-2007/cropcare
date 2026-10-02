import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "backend" / "cropcare.db"
DB.parent.mkdir(exist_ok=True)
if DB.exists():
    DB.unlink()          # start fresh, so running twice is safe

conn = sqlite3.connect(DB)
conn.executescript((ROOT / "database" / "schema.sql").read_text(encoding="utf-8"))
conn.executescript((ROOT / "database" / "seed_data.sql").read_text(encoding="utf-8"))
conn.commit()
print("Diseases stored:", conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0])
conn.close()