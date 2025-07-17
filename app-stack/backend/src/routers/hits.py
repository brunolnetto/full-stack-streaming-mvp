import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from models.hits import Hit
from services.db import get_hits

router = APIRouter(tags=["Hits"])

@router.get("/hits", response_model=List[Hit])
def hits():
    return [Hit(**hit) for hit in get_hits()] 