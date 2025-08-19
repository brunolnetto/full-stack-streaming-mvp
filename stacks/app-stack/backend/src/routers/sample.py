from fastapi import APIRouter
from models.sample import SampleResponse

router = APIRouter(tags=["Sample"])

@router.get("/sample", response_model=SampleResponse)
def sample():
    return SampleResponse(message="This is a sample backend response")

@router.get("/")
def root():
    return {"message": "Backend is running"} 