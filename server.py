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
    async with websockets.serve(chat, "0.0.0.0", 8000):
        await asyncio.Future()  # run forever

asyncio.run(main())
