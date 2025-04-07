from flask import Flask, jsonify, render_template, request
import sqlite3
from app import app

DB_PATH = "database/streams.db"

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def index():
    return render_template("index.html")

def get_date_range():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM Streams")
    result = cursor.fetchone()
    conn.close()

    if result:
        earliest, latest = result
        return {"earliest": earliest, "latest": latest}
    else:
        return {"earliest": None, "latest": None}

def get_top_artists(limit: int, from_date=None, to_date=None, sort_by='listen_time'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    order_by = "total_listen_time DESC" if sort_by == 'listen_time' else "stream_count DESC"
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

def get_top_albums(limit: int, from_date=None, to_date=None, sort_by='listen_time'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    order_by = "total_listen_time DESC" if sort_by == 'listen_time' else "stream_count DESC"
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

def get_top_songs(limit: int, from_date=None, to_date=None, sort_by='listen_time'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    order_by = "total_listen_time DESC" if sort_by == 'listen_time' else "stream_count DESC"
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

@app.route("/data", methods=["GET"])
def data_page():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    sort_by = request.args.get("sort", "listen_time")

    return render_template(
        "data.html",
        date_range=get_date_range(),
        top_artists=get_top_artists(10, from_date, to_date, sort_by),
        top_albums=get_top_albums(10, from_date, to_date, sort_by),
        top_songs=get_top_songs(10, from_date, to_date, sort_by),
        from_date=from_date,
        to_date=to_date,
        sort_by=sort_by
    )

@app.route("/data/artists", methods=["GET"])
def data_page_artists():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    sort_by = request.args.get("sort", "listen_time")

    return render_template(
        "data_artists.html",
        top_artists=get_top_artists(50, from_date, to_date, sort_by),
        date_range=get_date_range(),
        from_date=from_date,
        to_date=to_date,
        sort_by=sort_by
    )

@app.route("/data/albums", methods=["GET"])
def data_page_albums():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    sort_by = request.args.get("sort", "listen_time")

    return render_template(
        "data_albums.html",
        top_albums=get_top_albums(50, from_date, to_date, sort_by),
        date_range=get_date_range(),
        from_date=from_date,
        to_date=to_date,
        sort_by=sort_by
    )

@app.route("/data/songs", methods=["GET"])
def data_page_songs():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    sort_by = request.args.get("sort", "listen_time")

    return render_template(
        "data_songs.html",
        top_songs=get_top_songs(50, from_date, to_date, sort_by),
        date_range=get_date_range(),
        from_date=from_date,
        to_date=to_date,
        sort_by=sort_by
    )
