"""Run each statement in queries.sql against ecommerce.db and print the results."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "ecommerce.db"
QUERIES_PATH = Path(__file__).parent / "queries.sql"

conn = sqlite3.connect(DB_PATH)
statements = [s.strip() for s in QUERIES_PATH.read_text().split(";") if s.strip()]

for i, stmt in enumerate(statements, 1):
    sql = "\n".join(l for l in stmt.split("\n") if not l.strip().startswith("--")).strip()
    if not sql:
        continue
    print(f"--- Query {i} ---")
    cur = conn.execute(sql)
    print([d[0] for d in cur.description])
    for row in cur.fetchall():
        print(row)
    print()

conn.close()
