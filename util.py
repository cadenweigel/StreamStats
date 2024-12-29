import json
import os
from typing import List, Dict
from objects import *

def convertListenTime(listenTime: int):
    # Convert milliseconds to total seconds, hours
    seconds = listenTime // 1000
    hours = seconds // 3600

    # Calculate remaining minutes
    remainingSeconds = seconds % 3600
    minutes = remainingSeconds // 60

    # Return formatted string
    return f"{hours}h {minutes}m"

def convertListenTimeDays(listenTime: int):
    # Convert milliseconds to total seconds, hours, days
    seconds = listenTime // 1000
    hours = seconds // 3600
    days = seconds // 86400

    # Calculate remaining hours
    remainingSeconds = seconds % 86400
    hours = remainingSeconds // 3600

    # Calculate remaining minutes
    remainingSeconds %= 3600
    minutes = remainingSeconds // 60

    # Return formatted string
    return f"{days}d {hours}h {minutes}m"