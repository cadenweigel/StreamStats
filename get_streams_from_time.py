import sys
from typing import List
import parser
from objects import *

"""
Code to split streams given a date
"""

def getStreamsFromTime(streams: List[dict], time):
    """
    Given a list of dicts (streams) and a time, returns the streams within that timespan
    getStreamsFromTime(streams, 2024) -> returns all streams from 2024
    getStreamsFromTime(streams, 2024-01) -> returns all streams from January 2024
    getStreamsFromTime(streams, 2024-01-01) -> returns all streams from January 1st, 2024
    """
    validStreams = []
    for stream in streams:
        if stream["endTime"].startswith(time):
            validStreams.append(stream)
    return validStreams

def getStreamsFromInterval(streams: List[dict], startTime, endTime):
    """
    Given a list of dicts (streams) and a time interval, returns the streams within that timespan
    getStreamsFromTime(streams, 2023, 2024) -> returns all streams from January 1st, 2023 to December 31st, 2024
    getStreamsFromTime(streams, 2024-01, 2024-02) -> returns all streams from January 1st, 2024 to February 29th, 2024
    getStreamsFromTime(streams, 2024-01-01, 2024-01-31) -> returns all streams from January 1st, 2024 to January 31st, 2024
    """
    pass