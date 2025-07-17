from pydantic import BaseModel
from typing import Optional, List

class FlinkJob(BaseModel):
    id: str
    name: str
    state: str
    start_time: Optional[int]

class FlinkJobException(BaseModel):
    root_exception: Optional[str]
    timestamp: Optional[int]
    truncated: Optional[bool]
    all_exceptions: Optional[list] 