import os
import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from state import active_connections

WEBSOCKET_SESSION_TIMEOUT = os.getenv('WEBSOCKET_SESSION_TIMEOUT')

router = APIRouter()

@router.websocket("/ws/hits")
async def websocket_hits(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await asyncio.sleep(WEBSOCKET_SESSION_TIMEOUT)
    except WebSocketDisconnect:
        active_connections.remove(websocket) 