import pandas as pd

url = "https://www.hockey-reference.com/leagues/NHL_2025_skaters.html"
tables = pd.read_html(url, header=[0,1])

df = tables[0]

# Flatten multi-index columns into single strings
df.columns = ['_'.join([str(c) for c in col if c]) for col in df.columns]

# Select the correct columns by their flattened names
players = df[[
    "Unnamed: 1_level_0_Player",
    "Unnamed: 4_level_0_Pos",
    "Unnamed: 5_level_0_GP",
    "Faceoffs_FO%"
]].copy()

# Rename them into clean schema
players = players.rename(columns={
    "Unnamed: 1_level_0_Player": "player_name",
    "Unnamed: 4_level_0_Pos": "position",
    "Unnamed: 5_level_0_GP": "games_played",
    "Faceoffs_FO%": "season_faceoff_pct"
})

# Add placeholders for extra attributes
players["player_id"] = None
players["handedness"] = None
players["career_faceoff_pct"] = None

# Reorder columns
players = players[[
    "player_id", "player_name", "position",
    "career_faceoff_pct", "season_faceoff_pct",
    "games_played", "handedness"
]]

players.to_csv("players.csv", index=False)
print("Saved players.csv with full league roster + season FO% from Hockey Reference")






