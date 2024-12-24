import json
import sys
from typing import List
import parser
import misc_parsers as parser
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
    parser.sortSongs(Songs, 0, len(Songs.songs)-1)
    parser.sortArtists(Artists, 0, len(Artists.artists)-1)

    for i in range(5):
        print(Artists.artists[i].name, Artists.artists[i].streams)

if __name__ == "__main__":
    main()