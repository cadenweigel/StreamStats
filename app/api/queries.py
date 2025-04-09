import sqlite3
from datetime import datetime

DB_PATH = "database/streams.db"

def get_date_range():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM Streams")
    result = cursor.fetchone()
    conn.close()

    if result:
        earliest = datetime.strptime(result[0].rstrip('Z'), "%Y-%m-%dT%H:%M:%S") if result[0] else None
        latest = datetime.strptime(result[1].rstrip('Z'), "%Y-%m-%dT%H:%M:%S") if result[1] else None
        return {"earliest": earliest, "latest": latest}
    else:
        return {"earliest": None, "latest": None}

def get_top_artists(limit, from_date=None, to_date=None, sort_by='listen_time'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    order_by = {
        'listen_time': "total_listen_time DESC",
        'streams': "stream_count DESC",
        'name': "LOWER(s.artist_name) ASC"
    }.get(sort_by, "total_listen_time DESC")

    query = f"""
        SELECT s.artist_name, COUNT(*) as stream_count, SUM(s.ms_played) as total_listen_time
        FROM Streams s
        WHERE (? IS NULL OR s.timestamp >= ?)
          AND (? IS NULL OR s.timestamp <= ?)
        GROUP BY s.artist_name
        ORDER BY {order_by}
        LIMIT ?;
    """
    cursor.execute(query, (from_date, from_date, to_date, to_date, limit))
    results = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "streams": row[1], "listen_time": row[2]} for row in results]

def get_top_albums(limit, from_date=None, to_date=None, sort_by='listen_time'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    order_by = {
        'listen_time': "total_listen_time DESC",
        'streams': "stream_count DESC",
        'name': "LOWER(s.album_name) ASC"
    }.get(sort_by, "total_listen_time DESC")

    query = f"""
        SELECT s.album_name, s.artist_name, COUNT(*) as stream_count, SUM(s.ms_played) as total_listen_time
        FROM Streams s
        WHERE (? IS NULL OR s.timestamp >= ?)
          AND (? IS NULL OR s.timestamp <= ?)
        GROUP BY s.album_name, s.artist_name
        ORDER BY {order_by}
        LIMIT ?;
    """
    cursor.execute(query, (from_date, from_date, to_date, to_date, limit))
    results = cursor.fetchall()
    conn.close()
    return [
        {"name": row[0], "artist": row[1], "streams": row[2], "listen_time": row[3]}
        for row in results
    ]

def get_top_songs(limit, from_date=None, to_date=None, sort_by='listen_time'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    order_by = {
        'listen_time': "total_listen_time DESC",
        'streams': "stream_count DESC",
        'name': "LOWER(s.song_name) ASC"
    }.get(sort_by, "total_listen_time DESC")

    query = f"""
        SELECT s.song_name, s.artist_name, COUNT(*) as stream_count, SUM(s.ms_played) as total_listen_time
        FROM Streams s
        WHERE (? IS NULL OR s.timestamp >= ?)
          AND (? IS NULL OR s.timestamp <= ?)
        GROUP BY s.song_name, s.artist_name
        ORDER BY {order_by}
        LIMIT ?;
    """
    cursor.execute(query, (from_date, from_date, to_date, to_date, limit))
    results = cursor.fetchall()
    conn.close()
    return [
        {"name": row[0], "artist": row[1], "streams": row[2], "listen_time": row[3]}
        for row in results
    ]

def get_overall_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Streams")
    total_streams = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(ms_played) FROM Streams")
    total_listening_time = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(DISTINCT song_name || ' - ' || artist_name) FROM Streams")
    unique_songs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT album_name || ' - ' || artist_name) FROM Streams")
    unique_albums = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT artist_name) FROM Streams")
    unique_artists = cursor.fetchone()[0]

    conn.close()

    return {
        "total_streams": total_streams,
        "total_listening_time": total_listening_time,
        "unique_songs": unique_songs,
        "unique_albums": unique_albums,
        "unique_artists": unique_artists
    }
