# Faceoff Predictor

This project explores whether NHL faceoff outcomes can be predicted using player statistics, opponent statistics, zone information, and handedness. It includes a data preparation pipeline, a machine learning model, and a Streamlit interface for interacting with the model.

The goal of the project is to build a complete, end-to-end workflow:
- Data loading and merging
- Feature engineering and encoding
- Model training and evaluation
- Saving the trained model
- A simple UI for making predictions
- A deployed demo for documentation purposes

---

## Project Structure
app.py              # Streamlit UI for interacting with the model
train_model.py      # Model training script
faceoff_model.pkl   # Saved model artifact
requirements.txt    # Dependencies
data/               # CSV datasets (faceoff_data.csv, players.csv)


---

## Model Overview

The model is a RandomForestClassifier trained on merged player and opponent statistics.  
Categorical features (zone, handedness, position, etc.) are one-hot encoded.  
The script prints feature importances and saves the trained model as `faceoff_model.pkl`.

This project is still in progress. The current version focuses on establishing a working pipeline and UI.

---

## Streamlit Interface

The Streamlit app provides a simple form where users can input:
- Player ID  
- Opponent ID  
- Zone (defensive, neutral, offensive)  
- Handedness (left or right)

The interface will be updated to match the full feature set used during training.

---

## Deployment

A lightweight deployment will be added to provide a live demo and screenshot for documentation.  
The deployed version will run the Streamlit interface and load the trained model directly.

A link will be added here once deployment is complete.

---

## Next Steps

- Align Streamlit input features with the model’s training features  
- Improve feature engineering and data quality  
- Add a proper prediction endpoint  
- Deploy the full model  
- Update screenshots and documentation  

---

## Tech Stack

- Python  
- pandas  
- scikit-learn  
- numpy  
- Streamlit  



