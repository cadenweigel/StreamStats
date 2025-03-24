import os
import sqlite3
from pathlib import Path
import sys

# Add the project root to sys.path to allow importing from sibling folders
sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.init_database import initialize_db  # now this works!

TEST_DB_PATH = Path(__file__).resolve().parent.parent / "database" / "test_spotify.db"

def test_initialize():
    if TEST_DB_PATH.exists():
        os.remove(TEST_DB_PATH)

    initialize_db(str(TEST_DB_PATH))

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    required_tables = {"Streams", "Songs", "Artists", "Albums"}

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}

    missing = required_tables - tables
    assert not missing, f"Missing tables: {missing}"

    print("✅ All tables created successfully.")

    try:
        cursor.execute("""
            INSERT INTO Artists (artist_id, artist_name, listen_time, first_stream, last_stream, streams)
            VALUES ('artist_1', 'Test Artist', 100000, '2024-01-01', '2025-01-01', 10)
        """)
        print("✅ Insert into Artists passed.")
    except Exception as e:
        print("❌ Insert failed:", e)
    finally:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    test_initialize()
