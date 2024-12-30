import sys
import os
from typing import List
import parser
from objects import *
import get_streams_from_time as time
import util
import printer

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

    #get streams loaded into Artists and Songs, then sort
    parser.parseStreams(streams, Songs, Artists)
    parser.sortSongs(Songs, 0, len(Songs)-1)
    parser.sortArtists(Artists, 0, len(Artists)-1)

    #printer.printToTerminal(streams, Artists, Songs)
    printer.printToFile(streams, Artists, Songs)


if __name__ == "__main__":
    main()