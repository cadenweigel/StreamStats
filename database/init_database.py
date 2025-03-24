import json
import sys
import os

import sqlite3


"""
This file creates the database
doesn't need to be ran again since the database already exists
"""


def main():

    print("Initializing SQLite Database...")

    conn = sqlite3.connect("streams.db")  # creates/opens a database file
    cursor = conn.cursor()  # cursor is used to use SQL commands

    # Create tables
    cursor.executescript(
    """
    
    """
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()