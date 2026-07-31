"""Reset ecommerce.db from schema.sql. Run before a demo to get a clean seeded database."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "ecommerce.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

conn = sqlite3.connect(DB_PATH)
conn.executescript(SCHEMA_PATH.read_text())
conn.commit()
conn.close()
print(f"Reset {DB_PATH.name} from {SCHEMA_PATH.name}.")
