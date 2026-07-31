# CS4092 Project — E-Commerce Backend Database

Individual project for CS4092 Database Design and Development (Summer 2026).

## Files

| File | Deliverable |
|---|---|
| [requirements.md](requirements.md) / [requirements.pdf](requirements.pdf) | Requirements gathering |
| [er_diagram.md](er_diagram.md) / [er_diagram.png](er_diagram.png) | ER diagram |
| [schema.md](schema.md) / [schema.pdf](schema.pdf) | Relational schema |
| [schema.sql](schema.sql) | Schema creation + sample data (implementation) |
| [queries.sql](queries.sql) | SQL queries (4, incl. multi-table join) |
| [app.py](app.py) | Business-logic CLI (staff + customer roles) |
| [init_db.py](init_db.py) / [run_queries.py](run_queries.py) | Demo helper scripts |

## Why SQLite

The DBMS choice was SQLite, run through Python's built-in `sqlite3` module. It satisfies
the assignment's "any relational DBMS" requirement without needing a MySQL/Postgres
server installed and running. `schema.sql` is close to standard SQL — porting to
MySQL/Postgres would mainly mean swapping `AUTOINCREMENT` for `AUTO_INCREMENT` /
`SERIAL` and adjusting the `PRAGMA` line.

## Setup / Running

Requires Python 3 (no extra packages — `sqlite3` is in the standard library).

```bash
python app.py
```

On first run, `app.py` creates `ecommerce.db` next to it and seeds it from
`schema.sql` (2 staff, 3 customers, 5 products, 4 cards, 6 purchases). Delete
`ecommerce.db` at any time to reset to the seed data.

The CLI has two top-level roles:
- **Staff** — add a product, edit a product's price/stock, view inventory.
- **Customer** — pick a customer_id, browse products, add a credit card, purchase a
  product (validates stock and decrements it on purchase).

To reset the database from `schema.sql` or run the standalone queries, use the included
helper scripts (no `sqlite3` CLI required — both use Python's built-in `sqlite3` module):

```bash
python init_db.py
python run_queries.py
```

## Repo

This folder is a git repo pushed to GitHub with all deliverables committed.
