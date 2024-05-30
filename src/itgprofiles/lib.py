import asyncio
from pathlib import Path
import json

import websockets


def load_mapping(path: Path):
    return json.loads(path.read_text())["cards_to_profiles"]


async def websocket_client(uri, message):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        print(f"Sent message: {message}")


def set_player_profile(uri, player_number, profile_index):
    message = f"{player_number}:{profile_index}"
    asyncio.run(websocket_client(uri, message))
