import json
import sys
import os
import sqlite3

import process_data
from stream import Stream


def uploadStreams():
    """
    Uploads streams into the Streams table of streams.db
    Returns True if successful, False if not
    """

    streams_dict = process_data.getStreamsFiltered(30)
    streams = process_data.convertToStreamObjects(streams_dict)

    for s in streams:
        pass

    return True

def getArtists():
    """
    Gets artists formatted as Artist objects from Streams table
    """

    artists = []

    return artists

def uploadArtists():
    """
    Uploads Artist objects into Artists table
    This needs to be called before albums and songs
    """

    return True

def getAlbums():
    """
    Gets albums formatted as Album objects from Streams table
    Gets artist_id from Artists table (match with artist_name), so that needs to be populated first
    """

    albums = []

    return albums

def uploadAlbums():
    """
    Uploads Album objects into Albums table
    This needs to be called before songs
    """

    return True

def getSongs():
    """
    Gets songs formatted as Song objects from Streams table
    Gets artist_id from Artists table (match with artist_name in Streams, Artists)
    Gets album_id from Albums table (match with album_name in Streams, Albums)
    Treat the same song on different albums as separate for now, API will fix issue
    """

    songs = []

    return songs

def uploadSongs():
    """
    Uploads Song objects into Songs table
    """

    return True

def main():

    print("Uploading data...")
    #uploadStreams()
    #uploadArtists()
    #uploadAlbums()
    #uploadSongs()

if __name__ == "__main__":
    main()