#!/usr/bin/env python3
"""
Prints SQLite tables and sample rows from `backend/bookmyshoot.db`.
Run from project root or backend folder.
"""
import sqlite3
from pathlib import Path

# Try several common locations for the SQLite DB created by the app
possible_paths = [
    Path(__file__).parent / 'bookmyshoot.db',
    Path(__file__).parent / 'instance' / 'bookmyshoot.db',
    Path(__file__).parent.parent / 'instance' / 'bookmyshoot.db',
    Path(__file__).parent.parent / 'bookmyshoot.db'
]

DB_PATH = None
for p in possible_paths:
    if p.exists():
        DB_PATH = p
        break

if not DB_PATH:
    print('Database file not found in expected locations:')
    for p in possible_paths:
        print(' -', p)
    exit(1)

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()

# List tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
rows = cur.fetchall()
if not rows:
    print("No tables found in database.")
    conn.close()
    exit(0)

tables = [r[0] for r in rows]
print('Tables found:', tables)
print()

for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        count = cur.fetchone()[0]
    except Exception as e:
        print(f"Could not count rows for {t}: {e}")
        continue
    print(f"-- {t} (rows: {count})")
    # Show up to 5 rows
    try:
        cur.execute(f"SELECT * FROM {t} LIMIT 5")
        sample = cur.fetchall()
        if sample:
            # print column names
            cur2 = conn.execute(f"PRAGMA table_info({t})")
            cols = [c[1] for c in cur2.fetchall()]
            print(' | '.join(cols))
            for r in sample:
                print(' | '.join([str(x) if x is not None else 'NULL' for x in r]))
        else:
            print('  (no rows)')
    except Exception as e:
        print(f"  Could not fetch rows for {t}: {e}")
    print()

conn.close()
