from fastapi import APIRouter
import pickle
import os

router = APIRouter()

# Define or import the SampleModel class
class SampleModel:
    def get_data(self):
        # Implement the method to return data
        return {"example": "data"}

# Load the model from the pickle file
model_path = os.path.join(os.path.dirname(__file__), "models\model.pkl")
print(f'caminho: { model_path }')
with open(model_path, "rb") as model_file:
    model = pickle.load(model_file)

@router.get("/model/data")
async def get_model_data():
    # Assuming the model has a method to get data
    data = model.get_data()  # Replace with actual method to retrieve data
    return {"data": data}