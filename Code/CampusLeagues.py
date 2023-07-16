import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


class LeagueTable:

    def __init__(self, tableUrl, fixturesUrl, resultsUrl):
        self.tableUrl = tableUrl
        self.fixturesUrl = fixturesUrl
        self.resultsUrl = resultsUrl

        self.league = self.getTable(self.tableUrl)
        print(self.league)
        self.points = 0
        self.position = -1
        self.goalsFor = 0
        self.goalsAgainst = 0
        self.wins = 0
        self.loses = 0
        self.draws = 0
        self.fixtures = []
        self.results = []

    def getTable(self, url):
        res = requests.get(url)

        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')

            table = soup.find('table', class_="division-table")

            if table:
                # Initialize a list to store the table content
                table_content = []
                headers = []
                header_row = table.find('tr')
                for header in header_row.find_all('th'):
                    headers.append(header.text.strip())
                # Iterate through each row in the table
                for row in table.find_all('tr'):
                    # Extract data from each cell in the row
                    row_data = [cell.text.strip() for cell in row.find_all('td')]
                    table_content.append(row_data)

                df = pd.DataFrame(table_content, columns=headers)
                return df
            else:
                print(f"Table with class not found.")
                return None

    def points(self):
        return self.points

    def goalsFor(self):
        return self.goalsFor

    def goalsFor(self):
        return self.goalsFor

    def goalsAgainst(self):
        return self.goalsAgainst

    def wins(self):
        return self.wins

    def loses(self):
        return self.loses

    def draws(self):
        return self.draws

    def positions(self):
        return self.positions

    

CompSoc = LeagueTable("https://sportsheffield.sportpad.net/leagues/view/1450/84", "", "")
