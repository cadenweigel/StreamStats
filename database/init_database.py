import sqlite3

def initialize_db(db_path="database/streams.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Streams table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Streams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        song_name TEXT NOT NULL,
        artist_name TEXT NOT NULL,
        album_name TEXT,
        ms_played INTEGER NOT NULL,
        platform TEXT,
        reason_start TEXT,
        reason_end TEXT,
        shuffle BOOLEAN,
        skipped BOOLEAN,
        offline BOOLEAN
    );
    """)

    # Create Songs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Songs (
        song_id TEXT PRIMARY KEY,
        song_name TEXT,
        artist_id TEXT,
        album_id TEXT,
        listen_time INTEGER,
        first_stream TEXT,
        last_stream TEXT,
        streams INTEGER,
        FOREIGN KEY (artist_id) REFERENCES Artists(artist_id),
        FOREIGN KEY (album_id) REFERENCES Albums(album_id)
    );
    """)

    # Create Artists table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Artists (
        artist_id TEXT PRIMARY KEY,
        artist_name TEXT,
        listen_time INTEGER,
        first_stream TEXT,
        last_stream TEXT,
        streams INTEGER
    );
    """)

    # Create Albums table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Albums (
        album_id TEXT PRIMARY KEY,
        album_name TEXT,
        artist_id TEXT,
        listen_time INTEGER,
        first_stream TEXT,
        last_stream TEXT,
        streams INTEGER,
        FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
    );
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_db()
