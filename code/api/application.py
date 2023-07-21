import pandas as pd
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from ..webscraper import campus_leagues as cl

# Can add leagues here
compsoc = {
    "6s_Mon": cl.LeagueTable(
        "https://sportsheffield.sportpad.net/leagues/view/1426/84", "CompSoc Greens"),
    "11s": cl.LeagueTable(
        "https://sportsheffield.sportpad.net/leagues/view/1450/84", "Compsoc Greens"),
    "6s_Wed": cl.LeagueTable(
        "https://sportsheffield.sportpad.net/leaglsues/view/1432/84", "CompSoc Greens")
}
application = Flask(__name__)
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()


# curl "http://127.0.0.1:5000/api/table?league=6s_Mon" | jq to display in terminal
# curl "http://127.0.0.1:5000/api/table?league=6s_Wed" | jq to display in terminal
# curl "http://127.0.0.1:5000/api/table?league=11s" | jq to display in terminal
# Example endpoint that returns a JSON response
def update_league():
    global compsoc
    compsoc = {
        "6s_Mon": cl.LeagueTable(
            "https://sportsheffield.sportpad.net/leagues/view/1426/84", "CompSoc Greens"),
        "11s": cl.LeagueTable(
            "https://sportsheffield.sportpad.net/leagues/view/1450/84", "Compsoc Greens"),
        "6s_Wed": cl.LeagueTable(
            "https://sportsheffield.sportpad.net/leagues/view/1432/84", "CompSoc Greens")
    }


scheduler.add_job(update_league, trigger=IntervalTrigger(days=0.5))  # Will update the league


# All the get requests that will happen

@application.route("/api/table", methods=["GET"])
def get_table():
    league = request.args.get('league')
    table = compsoc[league].league_table.to_json()
    return table


@application.route("/api/wins", methods=["GET"])
def get_wins():
    league = request.args.get('league')
    return jsonify({"wins": compsoc[league].wins})


@application.route("/api/losses", methods=["GET"])
def get_losses():
    league = request.args.get('league')
    return jsonify({"losses": compsoc[league].losses})


@application.route("/api/draws", methods=["GET"])
def get_draws():
    league = request.args.get('league')
    return jsonify({"draws": compsoc[league].draws})


@application.route("/api/gf", methods=["GET"])
def get_gf():
    league = request.args.get('league')
    return jsonify({"goals_for": compsoc[league].goals_for})


@application.route("/api/ga", methods=["GET"])
def get_ga():
    league = request.args.get('league')
    return jsonify({"goals_against": compsoc[league].goals_against})


@application.route("/api/gd", methods=["GET"])
def get_gd():
    league = request.args.get('league')
    return jsonify({"goal_difference": compsoc[league].goal_difference})


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)
