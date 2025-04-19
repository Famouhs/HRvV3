import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_hr_odds():
    """
    Scrapes MLB home run odds from OddsJam or similar free sportsbook data.
    Returns a DataFrame with Player, Team, and HR odds.
    """
    url = "https://www.oddsjam.com/odds/player-props/mlb/home-run"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        raise RuntimeError(f"Failed to load odds page: {e}")

    players = []
    odds = []

    for prop in soup.select("div[class*=PlayerPropsRow]"):
        name_elem = prop.select_one("a[href*='/players/']")
        odds_elem = prop.select_one("div[class*=best-offer]")

        if name_elem and odds_elem:
            player = name_elem.text.strip()
            odd = odds_elem.text.strip()

            if "HR" in player.upper():
                continue  # filter out misparsed names

            players.append(player)
            odds.append(odd)

    df = pd.DataFrame({
        "Player": players,
        "HR_Odds": odds
    })

    return df
# TODO: Implement scraper
