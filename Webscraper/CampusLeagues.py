import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime

pd.set_option('display.max_colwidth', None)


def getTable(url):
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
            return df.iloc[1:]
        else:
            print(f"Table with class not found.")
            return None


def getResults(url):
    res = requests.get(url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'html.parser')

        table = soup.find('table', class_="fixtures list hidden-xs")
        tr_elements = table.find_all('tr', id='1306')

        team_a_list = []
        score_list = []
        team_b_list = []
        date = []
        date_format = "%A, %B %d, %Y"
        # Find all <tr> elements within the table
        tr_elements = table.find_all('tr', id=True)

        # Iterate through the <tr> elements to extract the required <td> elements
        for tr in tr_elements:
            prev_inner_header = tr.find_previous_sibling('tr', class_='inner-header')
            date_string = prev_inner_header.text.strip()
            parsed_date = datetime.strptime(date_string, date_format)
            output_date_string = parsed_date.strftime(date_format)
            date.append(str(parsed_date.date()))

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
                'Date': date
            })

        # Display the DataFrame
        return df


class LeagueTable:

    def __init__(self, tableUrl, teamName):
        self.fixtures = None
        self.results = None
        self.draws = None
        self.loses = None
        self.wins = None
        self.goalsAgainst = None
        self.goalsFor = None
        self.position = None
        self.points = None
        self.leagueTitle = None
        self.league = None

        self.tableUrl = tableUrl
        self.fixturesUrl = tableUrl.replace("view", "fixtures")
        self.resultsUrl = tableUrl.replace("view", "results")
        self.teamName = teamName

        self.set_all()

    def set_all(self):
        self.league = getTable(self.tableUrl)
        # print(self.league)
        row = self.league["Team"] == self.teamName

        greens = self.league[row]

        self.leagueTitle = self.getLeagueTitle(self.tableUrl)
        self.points = greens["Pts"].iloc[0]
        self.position = greens.index[0]
        self.goalsFor = greens["GA"].iloc[0]
        self.goalsAgainst = greens["GF"].iloc[0]
        self.wins = greens["W"].iloc[0]
        self.loses = greens["L"].iloc[0]
        self.draws = greens["D"].iloc[0]
        self.results = getResults(self.resultsUrl)
        self.fixtures = []

    def getLeagueTitle(self, url):
        res = requests.get(url)

        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')

            # Grab the h1 text from the soup object
            h1_text = soup.find('h1').text.strip()

            return h1_text
        else:
            print(f"Failed to fetch URL: {url}")
            return None

    def get_points(self):
        return self.points

    def get_goalsFor(self):
        return self.goalsFor

    def get_goalsFor(self):
        return self.goalsFor

    def get_goalsAgainst(self):
        return self.goalsAgainst

    def get_wins(self):
        return self.wins

    def get_loses(self):
        return self.loses

    def get_draws(self):
        return self.draws

    def get_positions(self):
        return self.positions

    def __str__(self):
        return (f"League Table: {self.leagueTitle}\n {self.league}\n"
                f"League Url: {self.tableUrl}\n"
                f"Points: {self.points}\n"
                f"Position: {self.position}\n"
                f"Goals For: {self.goalsFor}\n"
                f"Goals Against: {self.goalsAgainst}\n"
                f"Wins: {self.wins}\n"
                f"Loses: {self.loses}\n"
                f"Draws: {self.draws}\n"
                f"Fixtures:\n {self.fixtures}\n"
                f"Results: \n {self.results}")


