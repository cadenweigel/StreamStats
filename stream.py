import json
import sys
from typing import List
import parser
from objects import *

"""
Main file for parsing spotify data
End goal is to have this program format the data in a more accessible way
"""

def main():

    print("Welcome to the Stream Parser! :D")

    #Initialize Lists
    Artists: List[Artist] = []
    Songs: List[Song] = []

    #get streams information
    streams = parser.getStreams()
    bounds = parser.getStreamBounds(streams) #gives the dates that all streams occur within
    sys.setrecursionlimit(2000)

    #get streams loaded into Artists and Songs
    parser.parseStreams(streams, Songs, Artists)
    print("Total Streams: " + str(len(streams)))
    print("Total Artists: " + str(len(Artists)))
    print("Total Songs: " + str(len(Songs)))
    parser.sortSongs(Songs, 0, len(Songs)-1)
    parser.sortArtists(Artists, 0, len(Artists)-1)

    print("\n")
    for i in range(5):
        print(Artists[i].name, Artists[i].streams)

    print("\n")
    for i in range(5):
        print(Songs[i].artist, Songs[i].title, Songs[i].streams, Songs[i].listenTime)

if __name__ == "__main__":
    main()