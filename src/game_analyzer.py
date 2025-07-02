import pandas as pd
import json
import os

class GameAnalyzer:
    def __init__(self, game_id, df):
        self.game_id = game_id
        self.df = df
        self.home_team = df['home_team'].iloc[0]
        self.away_team = df['away_team'].iloc[0]
        self.score = 0