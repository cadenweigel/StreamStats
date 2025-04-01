import os
import sys

# Ensure 'database' is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from database import delete_database, init_database, upload_data

DB_PATH = "database/streams.db"

def delete_existing_db():
    delete_database.delete_sqlite_db(DB_PATH)

def init_db():
    print("Initializing new database...")
    init_database.initialize_db(DB_PATH)

def upload_all_data():
    print("Uploading data...")
    upload_data.set_db_path(DB_PATH)

    streams_dict = upload_data.process_data.getStreamsFiltered(30)
    streams = upload_data.process_data.convertToStreamObjects(streams_dict)

    artists = upload_data.getArtists(streams)
    albums = upload_data.getAlbums(streams, artists)
    songs = upload_data.getSongs(streams, artists)

    upload_data.uploadArtists(artists)
    upload_data.uploadAlbums(albums)
    upload_data.uploadSongs(songs)
    upload_data.uploadStreams(streams)

    print("Upload complete.")

if __name__ == "__main__":
    delete_existing_db()
    init_db()
    upload_all_data()
