import os
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
import uvicorn

def model_fn(model_dir: str):
    model_path = os.path.join(model_dir, "model.pkl")
    if not os.path.exists(model_path):
        raise RuntimeError(f"Model file not found at {model_path}")
    with open(model_path, "rb") as f:
        return pickle.load(f)

MODEL_DIR = os.environ.get("MODEL_DIR", "/app/model")
model = model_fn(MODEL_DIR)

app = FastAPI()

class PredictRequest(BaseModel):
    player_id: conint(ge=1)
    opponent_id: conint(ge=1)
    zone_defensive: conint(ge=0, le=1)
    zone_neutral: conint(ge=0, le=1)
    zone_offensive: conint(ge=0, le=1)
    handedness_left: conint(ge=0, le=1)
    handedness_right: conint(ge=0, le=1)

def validate_one_hot(zone_d: int, zone_n: int, zone_o: int, h_l: int, h_r: int) -> None:
    if (zone_d + zone_n + zone_o) != 1:
        raise HTTPException(
            status_code=400,
            detail="Zone flags must be one-hot: exactly one of defensive/neutral/offensive must be 1."
        )
    if (h_l + h_r) != 1:
        raise HTTPException(
            status_code=400,
            detail="Handedness flags must be one-hot: exactly one of left/right must be 1."
        )

@app.post("/predict")
def predict(req: PredictRequest):
    validate_one_hot(
        req.zone_defensive, req.zone_neutral, req.zone_offensive,
        req.handedness_left, req.handedness_right
    )

    feature_order = [
        "player_id",
        "opponent_id",
        "zone_defensive",
        "zone_neutral",
        "zone_offensive",
        "handedness_left",
        "handedness_right"
    ]

    data = pd.DataFrame(
        [[
            req.player_id,
            req.opponent_id,
            req.zone_defensive,
            req.zone_neutral,
            req.zone_offensive,
            req.handedness_left,
            req.handedness_right
        ]],
        columns=feature_order
    )

    try:
        pred = model.predict(data)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")

    result = "win" if int(pred) == 1 else "loss"
    return {
        "prediction": result,
        "message": f"Prediction complete: {result}"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)



