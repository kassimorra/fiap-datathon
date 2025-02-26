from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pipeline import run_all_process

app = FastAPI()

class ProcessResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None

@app.get("/updateDatabase", response_model=ProcessResponse)
async def update_database() -> ProcessResponse:
    try:
        run_all_process()
        return ProcessResponse(
            status="success",
            message="Database updated successfully",
            data=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Process failed: {str(e)}"
        )
