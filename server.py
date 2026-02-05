import os
import asyncio
import websockets

PORT = int(os.environ.get("PORT", 8000))
clients = set()

# Chat logic stays here
async def chat(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            for c in clients:
                if c != websocket:
                    await c.send(message)
    finally:
        clients.remove(websocket)

# This handler MUST have 2 arguments: websocket, path
async def handler(websocket, path):
    await chat(websocket)

# Start server with dynamic Railway port
async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())
