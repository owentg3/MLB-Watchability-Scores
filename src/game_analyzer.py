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
        self.scoring_breakdown = {}
    
    ##Helper Methods
    def get_half_inning_win_probs(df):
        df = df.copy()
        df['half_inning'] = df['inning_topbot'].str.lower().str[0] + df['inning'].astype(str)

        df['new_half_inning'] = df['half_inning'] != df['half_inning'].shift(1)

        starts = df[df['new_half_inning'] == True]

        win_probs = {}

        for _, row in starts.iterrows():
            key = row['half_inning']
            value = row['home_win_exp']
            if pd.notna(value):
                win_probs[key] = value

        return win_probs
    


    def calculate_score(self):
        self.score += self.score_hits()
        self.score += self.score_win_prob()
        self.score += self.score_close_game()
        self.score += self.score_walkoff()
        return self.score
    
    def score_hits(self):
        points = 0
        hit_events = self.df['events'].value_counts()
        scoring = {
            'single': 0.2,
            'double': 0.4,
            'triple': 0.7,
            'home_run': 2.5
        }
        for hit, value in scoring.items():
            count = hit_events.get(hit, 0)
            points += count * value
        self.scoring_breakdown['hit_score'] = points
        return points
    
    def score_win_prob(self):
        points = 0
        win_probs = self.get_half_inning_win_probs(self.df)
        