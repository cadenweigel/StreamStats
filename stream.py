import sys
from typing import List
import parser
from objects import *
import get_streams_from_time as time
import util

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

    #printToTerminal(streams, Artists, Songs)
    printToFile(streams, Artists, Songs)


def printToTerminal(streams, Artists, Songs):

    print("Total Streams: " + str(len(streams)))
    print("Total Artists: " + str(len(Artists)))
    print("Total Songs: " + str(len(Songs)))

    print("\n")
    for i in range(5):
        print(Artists[i].name, Artists[i].streams)

    print("\n")
    for i in range(5):
        print(Songs[i].artist, Songs[i].title, Songs[i].streams, Songs[i].listenTime)

def printToFile(streams, Artists, Songs):
    f = open("stream_report.txt", "w")
    f.write("Stream Data Report\n\n")

    f.write("Overall Stats:\n")
    f.write(f"Total Streams: {len(streams)}\n")
    f.write(f"Time Listened: {util.convertListenTimeDays(parser.sumListenTime(streams))}\n")
    f.write(f"Unique Artists: {len(Artists)}\n")
    f.write(f"Unique Songs: {len(Songs)}\n")

    # Format for the top artists
    f.write("Top Artists:\n\n")
    f.write(f"{'Artist':<20}{'Streams':>10}\n")
    f.write(f"{'-' * 30}\n")
    for i in range(5):
        f.write(f"{Artists[i].name:<20}{Artists[i].streams:>10}\n")
    f.write("\n\n")

    # Format for the top songs
    f.write("Top Songs:\n\n")
    f.write(f"{'Artist':<20}{'Title':<20}{'Streams':>10}{'Listen Time':>15}\n")
    f.write(f"{'-' * 65}\n")
    for i in range(5):
        f.write(f"{str(Songs[i].artist):<20}{Songs[i].title:<20}{Songs[i].streams:>10}{util.convertListenTime(Songs[i].listenTime):>15}\n")

    f.close()



if __name__ == "__main__":
    main()