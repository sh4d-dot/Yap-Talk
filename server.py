import asyncio
import websockets
import os

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

async def main():
    PORT = int(os.environ.get("PORT", 8000))
    async with websockets.serve(chat, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())

