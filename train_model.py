import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load datasets
df = pd.read_csv('faceoff_data.csv')
players = pd.read_csv('players.csv')

# Debug: print column names to confirm structure
print("Faceoff data columns:", df.columns.tolist())
print("Players data columns:", players.columns.tolist())

# Merge player stats
df = df.merge(players[["player_id", "player_name", "position", "season_faceoff_pct", "games_played", "handedness"]],
              on="player_id", how="left")

# Merge opponent stats (note: suffixes distinguish columns)
df = df.merge(players[["player_id", "player_name", "position", "season_faceoff_pct", "games_played", "handedness"]],
              left_on="opponent_id", right_on="player_id", how="left", suffixes=("", "_opp"))

# Inspect merged dataset
print("Merged dataset preview:")
print(df.head())

# Encode categorical features (both player and opponent)
df_encoded = pd.get_dummies(df, columns=['zone', 'handedness', 'position', 'handedness_opp', 'position_opp'])

# Inspect encoded dataset
print("Encoded dataset preview:")
print(df_encoded.head())

# Drop junk features (IDs and names don’t help prediction)
X = df_encoded.drop(['faceoff_win', 'player_id', 'opponent_id', 'player_name', 'player_id_opp', 'player_name_opp'], axis=1)
y = df_encoded['faceoff_win']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate accuracy
print("Test Accuracy:", model.score(X_test, y_test))

# Feature importance
importances = model.feature_importances_
feature_names = X.columns
sorted_idx = importances.argsort()[::-1]

print("Top feature importances:")
for idx in sorted_idx[:10]:
    print(f"{feature_names[idx]}: {importances[idx]:.4f}")

# Save model
with open('faceoff_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved as faceoff_model.pkl")
print("Features used:", X.columns.tolist())

