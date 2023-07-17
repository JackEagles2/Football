from flask import Flask, jsonify
from Webscraper import CampusLeagues as cl
import pandas

# curl "http://127.0.0.1:5000/api/table" | jq to display in terminal
CompSoc = cl.LeagueTable("https://sportsheffield.sportpad.net/leagues/view/1426/84", "CompSoc Greens")
app = Flask(__name__)


# Example endpoint that returns a JSON response
@app.route('/api/table', methods=['GET'])
def get_table():
    CompSoc.set_all()
    table = CompSoc.league.to_json()
    return table


@app.route('/api/wins', methods=['GET'])
def get_wins():
    # CompSoc.set_all()
    wins_data = CompSoc.get_wins()  # Call the wins() method from CompSoc
    return jsonify({"Wins": wins_data})


@app.route('/api/losses', methods=['GET'])
def get_losses():
    # CompSoc.set_all()
    losses_data = CompSoc.get_loses()  # Call the wins() method from CompSoc
    return jsonify({"Losses": losses_data})


@app.route('/api/draws', methods=['GET'])
def get_draws():
    # CompSoc.set_all()
    draws_data = CompSoc.get_draws()  # Call the wins() method from CompSoc
    return jsonify({"Draws": draws_data})


@app.route('/api/gf', methods=['GET'])
def get_gf():
    # CompSoc.set_all()
    ga_data = CompSoc.get_goalsFor()  # Call the wins() method from CompSoc
    return jsonify({"Goal For": ga_data})


@app.route('/api/ga', methods=['GET'])
def get_ga():
    # CompSoc.set_all()
    ga_data = CompSoc.get_goalsAgainst()  # Call the wins() method from CompSoc
    return jsonify({"Goal Against": ga_data})


@app.route('/api/gd', methods=['GET'])
def get_gd():
    # CompSoc.set_all()
    gd_data = CompSoc.get_goalsFor() - CompSoc.get_goalsAgainst()  # Call the wins() method from CompSoc
    return jsonify({"Goals Difference": gd_data})


if __name__ == '__main__':
    app.run()
