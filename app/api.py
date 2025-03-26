from flask import Flask, jsonify, render_template 
import sqlite3
from app import app

DB_PATH = "database/streams.db"

@app.route("/")
def index():
    return render_template("index.html")

def get_top_artists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT artist_name, streams FROM Artists
        ORDER BY streams DESC
        LIMIT 10;
    """)
    results = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "streams": row[1]} for row in results]

def get_top_albums():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Albums.album_name, Artists.artist_name, Albums.streams
        FROM Albums
        JOIN Artists ON Albums.artist_id = Artists.artist_id
        ORDER BY Albums.streams DESC
        LIMIT 10;
    """)
    results = cursor.fetchall()
    conn.close()
    return [
        {"name": row[0], "artist": row[1], "streams": row[2]}
        for row in results
    ]

def get_top_songs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Songs.song_name, Artists.artist_name, Songs.streams
        FROM Songs
        JOIN Artists ON Songs.artist_id = Artists.artist_id
        ORDER BY Songs.streams DESC
        LIMIT 10;
    """)
    results = cursor.fetchall()
    conn.close()
    return [
        {"name": row[0], "artist": row[1], "streams": row[2]}
        for row in results
    ]

@app.route("/data.json", methods=["GET"])
def get_data():
    return jsonify({
        "top_artists": get_top_artists(),
        "top_albums": get_top_albums(),
        "top_songs": get_top_songs()
    })

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/data", methods=["GET"])
def data_page():
    return render_template(
        "data.html",
        top_artists=get_top_artists(),
        top_albums=get_top_albums(),
        top_songs=get_top_songs()
    )