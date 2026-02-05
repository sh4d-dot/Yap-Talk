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

# No 'path' argument needed in new version
async def handler(websocket):
    await chat(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())
