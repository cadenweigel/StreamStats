from typing import List
import sqlite3

class Stream:
    
    def __init__(self, timestamp: str, platform: str, ms_played: int, country: str, 
                 track_name: str, artist_name: str, album_name: str, 
                 spotify_track_uri: str, reason_start: str, reason_end: str, 
                 shuffle: bool, skipped: bool, offline: bool):
        
        self.timestamp = timestamp
        self.platform = platform
        self.ms_played = ms_played
        self.country = country
        self.track_name = track_name
        self.artist_name = artist_name
        self.album_name = album_name
        self.spotify_track_uri = spotify_track_uri
        self.reason_start = reason_start
        self.reason_end = reason_end
        self.shuffle = shuffle
        self.skipped = skipped
        self.offline = offline

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "platform": self.platform,
            "ms_played": self.ms_played,
            "country": self.country,
            "track_name": self.track_name,
            "artist_name": self.artist_name,
            "album_name": self.album_name,
            "spotify_track_uri": self.spotify_track_uri,
            "reason_start": self.reason_start,
            "reason_end": self.reason_end,
            "shuffle": self.shuffle,
            "skipped": self.skipped,
            "offline": self.offline
        }
    
    def save_to_database(self, db_connection: sqlite3.Connection) -> bool:
        """Save stream to database"""
        if not db_connection:
            print("Database connection not provided")
            return False

        try:
            cursor = db_connection.cursor()

            #use cursor.execute to upload to database


            db_connection.commit()
            return True

        except Exception as e:
            print(f"Error storing trail analysis: {e}")
            if self.db:
                self.db.rollback()
            return False

