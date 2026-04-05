import pandas as pd
import random

zones = ['offensive', 'defensive', 'neutral']
handedness = ['left', 'right']
data = []

for _ in range(500):
    zone = random.choice(zones)
    player = random.randint(1, 30)
    opponent = random.randint(1, 30)
    hand = random.choice(handedness)
    win = random.choice([0, 1])

    data.append({
        'zone': zone,
        'player_id': player,
        'opponent_id': opponent,
        'handedness': hand,
        'faceoff_win': win
    })

df = pd.DataFrame(data)
df.to_csv('faceoff_data.csv', index=False)
print("Mock data generated: faceoff_data.csv")
