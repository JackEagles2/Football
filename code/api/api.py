import pandas as pd
from flask import Flask, jsonify

from ..webscraper import campus_leagues as cl

# curl "http://127.0.0.1:5000/api/table" | jq to display in terminal
compsoc = cl.LeagueTable(
    "https://sportsheffield.sportpad.net/leagues/view/1426/84", "CompSoc Greens"
)
app = Flask(__name__)


# Example endpoint that returns a JSON response
@app.route("/api/table", methods=["GET"])
def get_table():
    table = compsoc.league_table.to_json()
    return table


@app.route("/api/wins", methods=["GET"])
def get_wins():
    return jsonify({"wins": compsoc.wins})


@app.route("/api/losses", methods=["GET"])
def get_losses():
    return jsonify({"losses": compsoc.losses})


@app.route("/api/draws", methods=["GET"])
def get_draws():
    return jsonify({"draws": compsoc.draws})


@app.route("/api/gf", methods=["GET"])
def get_gf():
    return jsonify({"goals_for": compsoc.goals_for})


@app.route("/api/ga", methods=["GET"])
def get_ga():
    return jsonify({"goals_against": compsoc.goals_against})


@app.route("/api/gd", methods=["GET"])
def get_gd():
    return jsonify({"goal_difference": compsoc.goal_difference})


if __name__ == "__main__":
    app.run()
