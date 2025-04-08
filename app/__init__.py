from flask import Flask
from app.api.utils import format_milliseconds

app = Flask(__name__)

# Register custom Jinja filter for formatting time
app.jinja_env.filters['format_time'] = format_milliseconds

# Import routes to register them with the Flask app
from app.api.routes import *