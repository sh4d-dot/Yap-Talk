import os
PORT = int(os.environ.get("PORT", 8000))  # gets Railway’s assigned port

import asyncio
import websockets

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
    async with websockets.serve(chat, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())
