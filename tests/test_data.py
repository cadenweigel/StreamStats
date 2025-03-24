import json
import sys
import os

import stream
import process_json

def test_process():
    streams = process_json.getStreamsAll()
    print(f"Length of streams: {len(streams)}")
    filtered_streams_25s = process_json.getStreamsFiltered(25)
    print(f"Length of filtered streams (25s): {len(filtered_streams_25s)}")
    filtered_streams_30s = process_json.getStreamsFiltered(30)
    print(f"Length of filtered streams (30s): {len(filtered_streams_30s)}")

def main():
    test_process()

if __name__ == "__main__":
    main()