import pandas as pd

def get_player_stats():
    """
    Scrapes 2024 MLB batting stats (HR, AB, etc.) from FanGraphs.
    Returns a pandas DataFrame of the top 50 players.
    """
    url = (
        "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat"
        "&lg=all&qual=0&type=8&season=2024&month=0&season1=2024"
        "&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_50"
    )

    try:
        dfs = pd.read_html(url)
        df = dfs[11]  # The table is usually the 12th table on the page
    except Exception as e:
        raise RuntimeError(f"Failed to scrape FanGraphs data: {e}")

    # Clean column names and format
    df.columns = df.columns.droplevel(0)
    df.rename(columns={"Name": "Player", "Team": "Team"}, inplace=True)
    df = df[["Player", "Team", "HR", "AB", "PA", "SLG", "OPS"]]
    df = df.dropna(subset=["Player"])

    # Convert stat columns to numeric
    for col in ["HR", "AB", "PA", "SLG", "OPS"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
# TODO: Implement scraper
