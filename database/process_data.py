import json
import sys
import os
from typing import List, Dict

from database.stream import Stream

"""
Contains functions used for processing the stream json data
These functions are primarily used in upload_data.py
"""

def getFileAsDict(filename):
    #return file contents as a list of dictionaries
    with open(filename, 'r', encoding="utf8", errors="replace") as file:
        file_content = file.read()
    data = json.loads(file_content) #creates a list of dicts
    return data

def getStreamFiles():
    """
    gets any streaming history files and returns a list of strings
    want to automate it eventually (not type in file names manually)
    should be able to check string until it gets to a number
    SpotifyAccountData/StreamingHistory_music_ would indicate a valid file
    """
    files = os.listdir("streamdata")
    stream_files = []
    for f in files:
        if f.startswith("Streaming_History_Audio_"):
            #since the directory isn't included when doing os.listdir
            #it needs to be added back in the string
            stream_files.append("streamdata/" + f)

    return stream_files

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
        s = Stream(d['ts'], d['platform'], d['ms_played'], d['conn_country'],
                    d['master_metadata_track_name'],
                    d['master_metadata_album_artist_name'],
                    d['master_metadata_album_album_name'],
                    d['spotify_track_uri'], d['reason_start'], d['reason_end'],
                    d['shuffle'], d['skipped'], d['offline'])
        streams.append(s)

    return streams
