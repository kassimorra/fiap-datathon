from fastapi import FastAPI
import pickle
from api.endpoints import router as api_router

app = FastAPI()

# Load the model from the pickle file
with open("api/models/model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

app.include_router(api_router)