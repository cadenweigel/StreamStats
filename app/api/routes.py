from flask import request, jsonify, render_template
from app import app
from .queries import get_top_artists, get_top_albums, get_top_songs, get_date_range
from .queries import get_overall_stats 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET"])
def api_data():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    sort_by = request.args.get("sort", "listen_time")

    return jsonify({
        "top_artists": get_top_artists(25, from_date, to_date, sort_by),
        "top_albums": get_top_albums(25, from_date, to_date, sort_by),
        "top_songs": get_top_songs(25, from_date, to_date, sort_by),
    })

@app.route("/data", methods=["GET"])
def data_page():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    sort_by = request.args.get("sort", "listen_time")

    return render_template(
        "data.html",
        date_range=get_date_range(),
        top_artists=get_top_artists(25, from_date, to_date, sort_by),
        top_albums=get_top_albums(25, from_date, to_date, sort_by),
        top_songs=get_top_songs(25, from_date, to_date, sort_by),
        from_date=from_date,
        to_date=to_date,
        sort_by=sort_by
    )

@app.route("/overall_stats", methods=["GET"])
def overall_stats_page():
    stats = get_overall_stats()
    return render_template("overall_stats.html", stats=stats)

