import os
import sqlite3
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import init_database
from database.upload_data import (
    set_db_path,
    uploadStreams, uploadArtists, uploadAlbums, uploadSongs,
    getArtists, getAlbums, getSongs
)
from database.stream import Stream

TEST_DB_PATH = "tests/test_streams.db"

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create fresh test DB
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    init_database.initialize_db(TEST_DB_PATH)
    set_db_path(TEST_DB_PATH)
    yield
    # Clean up after test
    os.remove(TEST_DB_PATH)

def test_upload_all():
    streams = [
        Stream(
            timestamp="2024-01-01T12:00:00Z",
            platform="Spotify",
            ms_played=180000,
            country="US",
            track_name="Test Song",
            artist_name="Test Artist",
            album_name="Test Album",
            spotify_track_uri="spotify:track:123",
            reason_start="click-row",
            reason_end="trackdone",
            shuffle=False,
            skipped=False,
            offline=False
        )
    ]

    artists = getArtists(streams)
    albums = getAlbums(streams, artists)
    songs = getSongs(streams, artists)

    assert uploadArtists(artists)
    assert uploadAlbums(albums)
    assert uploadSongs(songs)
    assert uploadStreams(streams)

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Artists WHERE artist_name = ?", ("Test Artist",))
    assert cursor.fetchone() is not None

    cursor.execute("SELECT * FROM Albums WHERE album_name = ?", ("Test Album",))
    assert cursor.fetchone() is not None

    cursor.execute("SELECT * FROM Songs WHERE song_name = ?", ("Test Song",))
    assert cursor.fetchone() is not None

    cursor.execute("SELECT * FROM Streams WHERE song_name = ?", ("Test Song",))
    assert cursor.fetchone() is not None

    conn.close()
