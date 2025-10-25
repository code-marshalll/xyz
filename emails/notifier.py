import json
from typing import List
from fastapi import WebSocket

connected_clients: List[WebSocket] = []


async def broadcast_progress_update(progress: dict):
    """Send the latest progress to all connected websocket clients"""
    if not connected_clients:
        return
    data = json.dumps(progress)
    for ws in connected_clients.copy():
        try:
            await ws.send_text(data)
        except Exception:
            connected_clients.remove(ws)
