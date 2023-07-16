import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


class LeagueTable:

    def __init__(self, tableUrl):
        self.tableUrl = tableUrl
        self.fixturesUrl = tableUrl.replace("view", "fixtures")
        self.resultsUrl = tableUrl.replace("view", "results")

        self.league = self.getTable(self.tableUrl)
        # print(self.league)
        row = self.league["Team"] == "Compsoc Greens"

        greens = self.league[row]
        print(greens)
        self.points = greens["P"].iloc[0]
        self.position = greens.index[0]
        self.goalsFor = greens["GA"].iloc[0]
        self.goalsAgainst = greens["GF"].iloc[0]
        self.wins = greens["W"].iloc[0]
        self.loses = greens["L"].iloc[0]
        self.draws = greens["D"].iloc[0]
        self.results = self.getResults(self.resultsUrl)
        self.fixtures = []

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

    def getResults(self, url):

        res = requests.get(url)

        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')

            table = soup.find('table', class_="fixtures list hidden-xs")
            tr_elements = table.find_all('tr', id='1306')

            team_a_list = []
            score_list = []
            team_b_list = []
            date = []
            # Find all <tr> elements within the table
            tr_elements = table.find_all('tr', id=True)

            # Iterate through the <tr> elements to extract the required <td> elements
            for tr in tr_elements:
                prev_inner_header = tr.find_previous_sibling('tr', class_='inner-header')
                header_text = prev_inner_header.text.strip() if prev_inner_header else None
                date.append(header_text)

                # Find the <td> elements with the specified class names
                td_team_a = tr.find('td', class_='team-a no-width-truncate').text.strip()
                td_scores = tr.find_all('td', class_='score')
                td_team_b = tr.find('td', class_='team-b no-width-truncate').text.strip()

                score1 = td_scores[0].text.strip()
                score2 = td_scores[1].text.strip()
                formatted_score = f"{score1} - {score2}"
                # Append the data to the respective lists
                team_a_list.append(td_team_a)
                score_list.append(formatted_score)
                team_b_list.append(td_team_b)

                # Create a pandas DataFrame from the lists
                df = pd.DataFrame({
                    'Team A': team_a_list,
                    'Score': score_list,
                    'Team B': team_b_list,
                    'Date' : date
                })

            # Display the DataFrame
            return df

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

    def __str__(self):
        return (f"Points: {self.points}\n"
                f"Position: {self.position}\n"
                f"Goals For: {self.goalsFor}\n"
                f"Goals Against: {self.goalsAgainst}\n"
                f"Wins: {self.wins}\n"
                f"Loses: {self.loses}\n"
                f"Draws: {self.draws}\n"
                f"Fixtures:\n {self.fixtures}\n"
                f"Results: \n {self.results}")


CompSoc = LeagueTable("https://sportsheffield.sportpad.net/leagues/view/1450/84")

print(CompSoc)
