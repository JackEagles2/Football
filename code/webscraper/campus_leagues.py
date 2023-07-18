from datetime import datetime

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.set_option("display.max_colwidth", None)


def get_results(url):
    """Get results from the results page URL.

    Params:
        url (str): url of the results page.

    Returns:
        pd.DataFrame: data frame containing results data.
    """
    res = requests.get(url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "html.parser")

        table = soup.find("table", class_="fixtures list hidden-xs")
        tr_elements = table.find_all("tr", id="1306")

        team_a_list = []
        score_list = []
        team_b_list = []
        date = []
        date_format = "%A, %B %d, %Y"

        # find all <tr> elements within the table
        tr_elements = table.find_all("tr", id=True)

        # iterate through the <tr> elements to extract the required <td> elements
        for tr in tr_elements:
            prev_inner_header = tr.find_previous_sibling("tr", class_="inner-header")
            date_string = prev_inner_header.text.strip()
            parsed_date = datetime.strptime(date_string, date_format)
            output_date_string = parsed_date.strftime(date_format)
            date.append(str(parsed_date.date()))

            # find the <td> elements with the specified class names
            td_team_a = tr.find("td", class_="team-a no-width-truncate").text.strip()
            td_scores = tr.find_all("td", class_="score")
            td_team_b = tr.find("td", class_="team-b no-width-truncate").text.strip()

            score1 = td_scores[0].text.strip()
            score2 = td_scores[1].text.strip()
            formatted_score = f"{score1} - {score2}"

            # append the data to the respective lists
            team_a_list.append(td_team_a)
            score_list.append(formatted_score)
            team_b_list.append(td_team_b)

            # create a pandas DataFrame from the lists
            df = pd.DataFrame(
                {
                    "Team A": team_a_list,
                    "Score": score_list,
                    "Team B": team_b_list,
                    "Date": date,
                }
            )

        return df


class LeagueTable:
    """Class representing a league table from campus leagues website."""

    def __init__(self, table_url, team_name):
        """
        Params:
            table_url (str): url of the table.
            team_name (str): name of team you are interested in.
        """
        self.table_url = table_url
        self.fixtures_url = table_url.replace("view", "fixtures")
        self.results_url = table_url.replace("view", "results")
        self.team_name = team_name

        self._set_all()

    def _get_table(self):
        """Get the league table at the given URL.

        Returns:
            pd.DataFrame: data frame of the league table.
        """
        res = requests.get(self.table_url)

        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")

            table = soup.find("table", class_="division-table")

            if table:
                # initialize a list to store the table content
                table_content = []
                headers = []
                header_row = table.find("tr")
                for header in header_row.find_all("th"):
                    headers.append(header.text.strip())
                # iterate through each row in the table
                for row in table.find_all("tr"):
                    # extract data from each cell in the row
                    row_data = [cell.text.strip() for cell in row.find_all("td")]
                    table_content.append(row_data)

                df = pd.DataFrame(table_content, columns=headers)
                return df.iloc[1:]
            else:
                print(f"Table with class not found.")
                return None

    def _set_all(self):
        """Set all class variables based on team you are interested in."""
        self.league_table = self._get_table()
        row = self.league_table["Team"] == self.team_name

        greens = self.league_table[row]

        self.league_title = self._get_league_title()
        self.points = greens["Pts"].iloc[0]
        self.position = greens.index[0]
        self.goals_for = greens["GA"].iloc[0]
        self.goals_against = greens["GF"].iloc[0]
        self.wins = greens["W"].iloc[0]
        self.losses = greens["L"].iloc[0]
        self.draws = greens["D"].iloc[0]
        self.results = get_results(self.results_url)
        self.fixtures = []

    def _get_league_title(self):
        res = requests.get(self.table_url)

        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")

            # grab the h1 text from the soup object
            h1_text = soup.find("h1").text.strip()

            return h1_text
        else:
            print(f"Failed to fetch URL: {self.table_url}")
            return None

    @property
    def goal_difference(self):
        """Goal difference: gf - ga."""
        return int(self.goals_for) - int(self.goals_against)

    def __str__(self):
        return (
            f"League Table: {self.league_title}\n {self.league_table}\n"
            f"League Url: {self.table_url}\n"
            f"Points: {self.points}\n"
            f"Position: {self.position}\n"
            f"Goals For: {self.goals_for}\n"
            f"Goals Against: {self.goals_against}\n"
            f"Wins: {self.wins}\n"
            f"Losses: {self.losses}\n"
            f"Draws: {self.draws}\n"
            f"Fixtures:\n {self.fixtures}\n"
            f"Results: \n {self.results}"
        )
