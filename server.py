import os
import asyncio
import websockets
from http import HTTPStatus
from urllib.parse import urlparse

PORT = int(os.environ.get("PORT", 8000))
clients = set()

async def chat(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            for c in clients:
                if c != websocket:
                    await c.send(message)
    finally:
        clients.remove(websocket)

async def handler(websocket, path):
    # Only handle WebSocket upgrade requests
    if websocket.request_headers.get("Upgrade", "").lower() != "websocket":
        # Normal HTTP request → respond with a simple page
        await websocket.send("Hello! This is a WebSocket server. Use a WebSocket client to connect.")
        return
    await chat(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()

asyncio.run(main())
