import asyncio
import websockets

address, port = "localhost", 5555
connected_clients = set()


async def broadcast(message):
    if connected_clients:
        await asyncio.wait([asyncio.create_task(client.send(message)) for client in connected_clients])


async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            await broadcast(message)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {e}")
    finally:
        connected_clients.remove(websocket)


async def main():
    start_server = await websockets.serve(handler, address, port)
    print(f"WebSocket server started on ws://{address}:{port}")
    await start_server.wait_closed()


asyncio.run(main())
