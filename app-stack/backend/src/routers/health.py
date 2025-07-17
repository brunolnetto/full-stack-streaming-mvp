from fastapi import APIRouter
from models.health import HealthStatus

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthStatus)
def health():
    return HealthStatus(status="ok") 