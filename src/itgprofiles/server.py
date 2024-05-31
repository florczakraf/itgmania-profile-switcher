import argparse
import asyncio
import websockets

from itgprofiles.consts import WS_HOST, WS_PORT


class BroadcastingServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._connected_clients = set()

    async def run(self):
        return await websockets.serve(self._handler, self._host, self._port)

    async def _handler(self, websocket: websockets.WebSocketServerProtocol, _):
        self._connected_clients.add(websocket)
        try:
            async for message in websocket:
                print(f"[{websocket.server_header} - {websocket.remote_address}] Received message: {message}")
                websockets.broadcast(self._connected_clients, message)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Client disconnected: {e}")
        finally:
            self._connected_clients.remove(websocket)
            print(f"removed {websocket}")



def _get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--host", default=WS_HOST, help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=WS_PORT, help="Port to bind the server to")

    return parser


async def _inner_main(args):
    server = BroadcastingServer(args.host, args.port)
    server_loop = await server.run()
    print(f"Profile Switcher WebSocket server started on ws://{args.host}:{args.port}")
    await server_loop.wait_closed()


def main():
    parser = _get_parser()
    args = parser.parse_args()
    asyncio.run(_inner_main(args))


if __name__ == "__main__":
    main()
