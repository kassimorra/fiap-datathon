from fastapi import FastAPI
from _model import get_prediction

app = FastAPI()

@app.get("/getPrediction/{userid}")
async def read_root(userid: str):
    predict: dict = get_prediction(userid)
    return {"user_id": userid, "predictions": predict}