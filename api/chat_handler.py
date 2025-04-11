import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends,  Query, HTTPException
from websocket.manager import ConnectionManager 
from utils.settings import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

from typing import Optional


chat_handler = APIRouter()

manager = ConnectionManager()

async def get_current_user_from_token(
    websocket: WebSocket, token: Optional[str] = Query(None)
):
    """
    Extracts the token from the WebSocket URL query parameter,
    decodes it, and returns the user.
    """
    if not token:
        raise HTTPException(status_code=400, detail="Token is required")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
@chat_handler.websocket('/ws/notification')
async def websocket_notification(
    websocket: WebSocket):

    await manager.connect_notification(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Received your message: {data}")

    except Exception:
        # Handle disconnects, errors, etc.
        pass
    finally:
        # Remove the websocket from the active connections
        manager.disconnect(websocket)
    
@chat_handler.websocket('/ws/{room_id}')
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: str, 
    username: str = Depends(get_current_user_from_token)):

    await manager.connect(websocket, room_id, username)
    try:
        while True:
            data = await websocket.receive_text()
            if not data.strip():
                continue
            try:
                parsed = json.loads(data)
                await manager.send_message(websocket, parsed, room_id)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid JSON"}))
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id)

