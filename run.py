from flask import Flask, render_template
import os

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

@app.route("/")
def home():
    return render_template("index.html")

from app import app  # grabs it from app/__init__.py
from app import api  # registers the routes

if __name__ == "__main__":
    app.run(debug=True)

