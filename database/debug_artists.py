import os
import sys

# Make sure the root directory is in the path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from database import upload_data

def debug_artist_names():
    print("🔍 Getting Stream objects...")
    streams_dict = upload_data.process_data.getStreamsFiltered(30)
    streams = upload_data.process_data.convertToStreamObjects(streams_dict)

    print(f"\nLoaded {len(streams)} stream(s).")

    artists = upload_data.getArtists(streams)

    print(f"\nFound {len(artists)} artists. Listing names:\n")

    bad_artists = []
    for i, artist in enumerate(artists):
        name = artist.name
        if name is None:
            print(f"{i}: ❌ MISSING NAME (None)")
            bad_artists.append(None)
        elif not name.strip():
            print(f"{i}: ⚠️ EMPTY NAME (whitespace)")
            bad_artists.append("")
        else:
            print(f"{i}: {name}")

    if bad_artists:
        print("\n🔎 Searching for streams with missing or empty artist names:\n")
        for i, s in enumerate(streams):
            if s.artist_name is None:
                print(f"{i}: ❌ Stream with artist_name=None")
                print(f"  Timestamp: {s.timestamp}")
                print(f"  Track: {s.track_name}")
                print(f"  Album: {s.album_name}")
                print(f"  URI: {s.spotify_track_uri}")
                print()
            elif not s.artist_name.strip():
                print(f"{i}: ⚠️ Stream with empty artist_name")
                print(f"  Timestamp: {s.timestamp}")
                print(f"  Track: {s.track_name}")
                print(f"  Album: {s.album_name}")
                print(f"  URI: {s.spotify_track_uri}")
                print()

    else:
        print("\n✅ No broken artist names found in streams.")

if __name__ == "__main__":
    debug_artist_names()
