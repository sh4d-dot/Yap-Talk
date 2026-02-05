import os
import asyncio
import websockets

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

# handler must have 2 arguments: websocket and path
async def handler(websocket, path):
    await chat(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # keep server running forever

asyncio.run(main())
