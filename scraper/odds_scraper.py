import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_odds_data():
    """
    Scrapes home run prop odds from a free source like OddsJam or other sportsbook comparison sites.
    Returns a DataFrame with player names and home run odds.
    """
    url = "https://www.oddschecker.com/baseball/mlb/player/home-runs"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch odds data: Status code {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")

    # This parsing depends on the site structure, update selectors as needed
    odds_data = []
    markets = soup.find_all("div", class_="matchup-odds")

    for market in markets:
        player_tag = market.find("span", class_="player-name")
        odds_tag = market.find("span", class_="odds")

        if player_tag and odds_tag:
            player_name = player_tag.text.strip()
            odds = odds_tag.text.strip()
            odds_data.append({
                "Player": player_name,
                "HR_Odds": odds
            })

    odds_df = pd.DataFrame(odds_data)
    return odds_df
