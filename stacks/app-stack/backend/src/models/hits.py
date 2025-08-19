from pydantic import BaseModel
from typing import Optional

class Hit(BaseModel):
    route: str
    num_hits: int
    event_hour: Optional[str] 