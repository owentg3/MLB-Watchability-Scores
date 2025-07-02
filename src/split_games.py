import pandas as pd
import os
def split_statcast_by_game(file_path, output_dir = "data/processed"):
    df = pd.read_csv(file_path)
    os.makedirs(output_dir, exist_ok = True)

    for game_id in df['game_pk'].unique():
        game_df = df[df['game_pk'] == game_id]
        game_df.to_csv(f"{output_dir}/game_{game_id}.csv", index = False)
        print(f"Saved game {game_id} data.")

if __name__ == "__main__":
    split_statcast_by_game("data/raw/statcast_2025-06-29.csv")