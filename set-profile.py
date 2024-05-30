import asyncio
import websockets
import sys

async def test_client():
    uri = "ws://localhost:5555"
    async with websockets.connect(uri) as websocket:
        message = sys.argv[1]
        await websocket.send(message)
        print(f"Sent message: {message}")



asyncio.run(test_client())
