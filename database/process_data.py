import json
import sys
import os
from typing import List, Dict

from database.stream import Stream

"""
Contains functions used for processing the stream json data
These functions are primarily used in upload_data.py
"""

def getStreamFiles():
    """Gets full paths to all JSON files in the streamdata directory."""
    base_dir = os.path.dirname(__file__)  # -> .../database
    streamdata_dir = os.path.abspath(os.path.join(base_dir, "..", "streamdata"))

    if not os.path.exists(streamdata_dir):
        raise FileNotFoundError(f"'streamdata' directory not found at: {streamdata_dir}")

    files = [
        os.path.join(streamdata_dir, f)
        for f in os.listdir(streamdata_dir)
        if f.endswith(".json")
    ]
    return sorted(files)


def getFileAsDict(filename):
    """Loads a single JSON file and returns its contents as a Python dict."""
    with open(filename, 'r', encoding="utf8", errors="replace") as file:
        return json.load(file)

def getStreamsAll():

    files = [] #list of json files that will be parsed
    fileDicts: List[Dict] = [] #list of dictionaries that are returned from getFileAsDict

    files = getStreamFiles()
    for f in files:
        fileDicts.append(getFileAsDict(f))

    streams: List[Dict] = []
    for d in fileDicts:
        streams += d #add every dict in d to streams

    return streams

def getStreamsFiltered(seconds):

    files = [] #list of json files that will be parsed
    fileDicts: List[Dict] = [] #list of dictionaries that are returned from getFileAsDict

    files = getStreamFiles()
    for f in files:
        fileDicts.append(getFileAsDict(f))

    streams: List[Dict] = []
    for d in fileDicts:
        streams += d #add every dict in d to streams

    filtered = []
    ms_filter = seconds * 1000

    for s in streams:
        if s['ms_played'] >= ms_filter:
            filtered.append(s)

    return filtered

def convertToStreamObjects(data):
    """converts array of dictionaries to an array of Stream objects"""

    streams = []

    for d in data:
        artist = d.get('master_metadata_album_artist_name')
        if not artist or not artist.strip():
            continue  # Skip if artist is None or empty

        s = Stream(d['ts'], d['platform'], d['ms_played'], d['conn_country'],
                   d['master_metadata_track_name'],
                   artist,
                   d['master_metadata_album_album_name'],
                   d['spotify_track_uri'], d['reason_start'], d['reason_end'],
                   d['shuffle'], d['skipped'], d['offline'])
        streams.append(s)

    return streams
