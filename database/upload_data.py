import json
import sys
import os
import sqlite3
from typing import List
import hashlib

from database import process_data
from database.stream import Stream, Song, Album, Artist

DB_PATH = "database/streams.db"  # default

def set_db_path(path: str):
    global DB_PATH
    DB_PATH = path


def generate_id(*args):
    raw = ''.join(args)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def uploadStreams(data: List[Stream]):
    """
    Uploads streams into the Streams table of streams.db
    Returns True if successful, False if not
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for s in data:
            cursor.execute("""
                INSERT INTO Streams (
                    timestamp, song_name, artist_name, album_name,
                    ms_played, platform, reason_start, reason_end,
                    shuffle, skipped, offline
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s.timestamp, s.track_name, s.artist_name, s.album_name,
                s.ms_played, s.platform, s.reason_start, s.reason_end,
                s.shuffle, s.skipped, s.offline
            ))

        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print("UploadStreams error:", e)
        return False

def findArtist(artists: List[Artist], name) -> Artist:
    for a in artists:
        if a.name == name:
            return a
    return None

def getArtists(streams: List[Stream]) -> List[Artist]:

    artists = []

    for s in streams:

        artist = findArtist(artists, s.artist_name)

        if not artist:
            #init listen time and streams to 0 since it'll increment after
            artist = Artist(s.artist_name, 0, s.timestamp, s.timestamp, 0)
            artists.append(artist)

        artist.listen_time += s.ms_played
        artist.last_stream = s.timestamp
        artist.streams += 1

    return artists

def uploadArtists(data: List[Artist]):
    """
    Uploads Artist objects into Artists table
    This needs to be called before albums and songs
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for a in data:
            artist_id = generate_id(a.name)
            cursor.execute("""
                INSERT OR IGNORE INTO Artists (
                    artist_id, artist_name, listen_time,
                    first_stream, last_stream, streams
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                artist_id, a.name, a.listen_time,
                a.first_stream, a.last_stream, a.streams
            ))

        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print("UploadArtists error:", e)
        return False


def findAlbum(albums: List[Album], album_name, artist_name) -> Album:
    for a in albums:
        if a.name == album_name and a.artist_name == artist_name:
            return a
    return None

def getAlbums(streams: List[Stream], artists: List[Artist]) -> List[Album]:

    albums = []

    for s in streams:

        album = findAlbum(albums, s.album_name, s.artist_name)

        if not album:
            album = Album(s.album_name, s.artist_name, 0, s.timestamp, s.timestamp, 0)
            albums.append(album)

        album.listen_time = s.ms_played
        album.last_stream = s.timestamp
        album.streams += 1

    return albums

def uploadAlbums(data: List[Album]):
    """
    Uploads Album objects into Albums table
    This needs to be called before songs
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for a in data:
            album_id = generate_id(a.name, a.artist_name)
            artist_id = generate_id(a.artist_name)
            cursor.execute("""
                INSERT OR IGNORE INTO Albums (
                    album_id, album_name, artist_id,
                    listen_time, first_stream, last_stream, streams
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                album_id, a.name, artist_id,
                a.listen_time, a.first_stream, a.last_stream, a.streams
            ))

        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print("UploadAlbums error:", e)
        return False


def findSong(songs: List[Song], song_name, artist_name) -> Song:
    for s in songs:
        if s.name == song_name and s.artist_name == artist_name:
            return s
    return None

def getSongs(streams: List[Stream], artists: List[Artist]) -> List[Song]:

    songs = []

    for s in streams:

        song = findSong(songs, s.track_name, s.artist_name)

        if not song:
            song = Song(s.track_name, s.artist_name, 0, s.timestamp, s.timestamp, 0)
            songs.append(song)

        song.listen_time += s.ms_played
        song.last_stream = s.timestamp
        song.streams += 1

    return songs

def uploadSongs(data: List[Song]):
    """
    Uploads Song objects into Songs table
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for s in data:
            song_id = generate_id(s.name, s.artist_name)
            artist_id = generate_id(s.artist_name)
            album_id = None  # Could be included later if available
            cursor.execute("""
                INSERT OR IGNORE INTO Songs (
                    song_id, song_name, artist_id, album_id,
                    listen_time, first_stream, last_stream, streams
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                song_id, s.name, artist_id, album_id,
                s.listen_time, s.first_stream, s.last_stream, s.streams
            ))

        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print("UploadSongs error:", e)
        return False

def main():

    #get Stream objects
    streams_dict = process_data.getStreamsFiltered(30)
    streams = process_data.convertToStreamObjects(streams_dict)

    #use Stream objects to get data on Artists, Albums, and Songs
    artists = getArtists(streams)
    albums = getAlbums(streams, artists)
    songs = getSongs(streams, artists)

    uploadStreams(streams)
    uploadArtists(streams)
    uploadAlbums(streams)
    uploadSongs(streams)

if __name__ == "__main__":
    main()