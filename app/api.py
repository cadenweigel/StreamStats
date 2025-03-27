from flask import Flask, jsonify, render_template 
import sqlite3
from app import app

DB_PATH = "database/streams.db"

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def index():
    return render_template("index.html")

def get_top_artists(limit: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT artist_name, streams FROM Artists
        ORDER BY streams DESC
        LIMIT ?;
    """, (limit,))
    results = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "streams": row[1]} for row in results]

def get_top_albums(limit: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Albums.album_name, Artists.artist_name, Albums.streams
        FROM Albums
        JOIN Artists ON Albums.artist_id = Artists.artist_id
        ORDER BY Albums.streams DESC
        LIMIT ?;
    """, (limit,))
    results = cursor.fetchall()
    conn.close()
    return [
        {"name": row[0], "artist": row[1], "streams": row[2]}
        for row in results
    ]

def get_top_songs(limit: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Songs.song_name, Artists.artist_name, Songs.streams
        FROM Songs
        JOIN Artists ON Songs.artist_id = Artists.artist_id
        ORDER BY Songs.streams DESC
        LIMIT ?;
    """, (limit,))
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

@app.route("/data", methods=["GET"])
def data_page():
    return render_template(
        "data.html",
        top_artists=get_top_artists(10),
        top_albums=get_top_albums(10),
        top_songs=get_top_songs(10)
    )

@app.route("/data/artists", methods=["GET"])
def data_page_artists():
    return render_template(
        "data_artists.html",
        top_artists=get_top_artists(50)
    )

@app.route("/data/albums", methods=["GET"])
def data_page_albums():
    return render_template(
        "data_albums.html",
        top_albums=get_top_albums(50)
    )

@app.route("/data/songs", methods=["GET"])
def data_page_songs():
    return render_template(
        "data_songs.html",
        top_songs=get_top_songs(50)
    )