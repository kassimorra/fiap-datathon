from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from _feast_materialize import materialize_feature_view
from _get_features import get_user_features

app = FastAPI()

class ProcessResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None

@app.get("/materialize")
async def materialize() -> ProcessResponse:
    try:
        materialize_feature_view()
        return ProcessResponse(
            status="success",
            message="Feature updated successfully",
            data=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Process failed: {str(e)}"
        )
    
@app.get("/getfeatures/{userid}")
async def get_features(userid: str):
    features: dict = get_user_features(userid)
    return {"user_id": userid, "features": features}