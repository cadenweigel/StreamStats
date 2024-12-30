import json
import os
from typing import List, Dict
from objects import *
import parser
import util

"""
Contains various print functions for stream report
"""

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
    writeHeader(streams, Artists, Songs, f)
    writeArtists(streams, Artists, Songs, f)
    writeSongs(streams, Artists, Songs, f)
    f.close()


def writeHeader(streams, Artists, Songs, f):

    name = util.getUsername()
    bounds = parser.getStreamBounds(streams)

    f.write(f"Stream Data Report for {name}\n\n")

    f.write("Overall Stats:\n")
    f.write(f"Total Streams: {len(streams)}\n")
    f.write(f"Time Listened: {util.convertListenTimeDays(parser.sumListenTime(streams))}\n")
    f.write(f"Unique Artists: {len(Artists)}\n")
    f.write(f"Unique Songs: {len(Songs)}\n")
    f.write(f"Dates Listened: {bounds[0]} to {bounds[1]} \n")
    f.write("\n")


def writeArtists(streams, Artists, Songs, f):

    # Format for the top artists
    f.write("Top Artists:\n\n")
    f.write(f"{'Artist':<20}{'Streams':>10}{'Listen Time':>15}\n")
    f.write(f"{'-' * 45}\n")
    for i in range(5):
        f.write(f"{Artists[i].name:<20}{Artists[i].streams:>10}{util.convertListenTime(Artists[i].listenTime):>15}\n")
    f.write("\n\n")


def writeSongs(streams, Artists, Songs, f):

    # Format for the top songs
    f.write("Top Songs:\n\n")
    f.write(f"{'Artist':<20}{'Title':<20}{'Streams':>10}{'Listen Time':>15}\n")
    f.write(f"{'-' * 65}\n")
    for i in range(5):
        f.write(f"{str(Songs[i].artist):<20}{Songs[i].title:<20}{Songs[i].streams:>10}{util.convertListenTime(Songs[i].listenTime):>15}\n")
