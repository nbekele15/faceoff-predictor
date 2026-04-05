import streamlit as st
import requests

st.set_page_config(page_title="Faceoff Predictor", page_icon="🏒")
st.title("Faceoff Predictor")

col1, col2 = st.columns(2)
with col1:
    player_id = st.number_input("Player ID", min_value=1, step=1)
    zone = st.selectbox("Zone", ["defensive", "neutral", "offensive"])
with col2:
    opponent_id = st.number_input("Opponent ID", min_value=1, step=1)
    handedness = st.selectbox("Handedness", ["left", "right"])

def payload():
    return {
        "player_id": int(player_id),
        "opponent_id": int(opponent_id),
        "zone_defensive": 1 if zone == "defensive" else 0,
        "zone_neutral": 1 if zone == "neutral" else 0,
        "zone_offensive": 1 if zone == "offensive" else 0,
        "handedness_left": 1 if handedness == "left" else 0,
        "handedness_right": 1 if handedness == "right" else 0
    }

if st.button("Predict"):
    try:
        resp = requests.post("http://localhost:8080/predict", json=payload(), timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"Prediction: {data.get('prediction')}")
            st.caption(data.get('message'))
        else:
            st.error(f"API error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
