from flask import Flask

app = Flask(__name__)

from datetime import timedelta

def format_milliseconds(ms):
    seconds = int(ms / 1000)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"

app.jinja_env.filters['format_time'] = format_milliseconds
