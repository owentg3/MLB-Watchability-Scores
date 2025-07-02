from pybaseball import schedule_and_record, statcast
from datetime import datetime, timedelta
import pandas as pd
import os

def get_todays_schedule(teams):
    today = datetime.today().date()
    all_games = []

    for team in teams:
        try:
            schedule = schedule_and_record(today.year, team)
            games_today = schedule[schedule['Date'].dt.date == today]
            if not games_today.empty:
                all_games.append(games_today)
        except Exception as e:
            print(f"Error getting schedule for {team}: {e}")
        
        if all_games:
            df = pd.concat(all_games)
            os.makedirs("data/raw", exist_ok=True)
            df.to_csv(f"data/raw/schedule_{today}.csv", index = False)
            print(f"Saved schedule for {today}")
            return df
        else:
            print("No games found today.")
            return pd.DataFrame()
        
def get_todays_statCast(days_ago=2):
    # Calculate date X days ago
    target_date = datetime.now() - timedelta(days=days_ago)
    date_str = target_date.strftime('%Y-%m-%d')

    print(f"Today's date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Pulling Statcast data for: {date_str}")

    try:
        df = statcast(start_dt=date_str, end_dt=date_str)
        os.makedirs("data/raw", exist_ok=True)
        save_path = f"data/raw/statcast_{date_str}.csv"
        df.to_csv(save_path, index=False)
        print(f"✅ Saved statcast data to {save_path}")
        return df
    except Exception as e:
        print(f"❌ Error pulling statcast data: {e}")
        return pd.DataFrame()
    
if __name__ == "__main__":
    teams = [
        "ARI",  # Arizona Diamondbacks
        "ATL",  # Atlanta Braves
        "BAL",  # Baltimore Orioles
        "BOS",  # Boston Red Sox
        "CHC",  # Chicago Cubs
        "CIN",  # Cincinnati Reds
        "CLE",  # Cleveland Guardians
        "COL",  # Colorado Rockies
        "CWS",  # Chicago White Sox
        "DET",  # Detroit Tigers
        "HOU",  # Houston Astros
        "KC",   # Kansas City Royals
        "LAA",  # Los Angeles Angels
        "LAD",  # Los Angeles Dodgers
        "MIA",  # Miami Marlins
        "MIL",  # Milwaukee Brewers
        "MIN",  # Minnesota Twins
        "NYM",  # New York Mets
        "NYY",  # New York Yankees
        "OAK",  # Oakland Athletics
        "PHI",  # Philadelphia Phillies
        "PIT",  # Pittsburgh Pirates
        "SD",   # San Diego Padres
        "SEA",  # Seattle Mariners
        "SF",   # San Francisco Giants
        "STL",  # St. Louis Cardinals
        "TB",   # Tampa Bay Rays
        "TEX",  # Texas Rangers
        "TOR",  # Toronto Blue Jays
        "WSH",  # Washington Nationals
    ]
    
    schedule_df = get_todays_schedule(teams)
    statcast_df = get_todays_statCast()