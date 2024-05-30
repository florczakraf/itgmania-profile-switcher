import argparse
import asyncio
import websockets

from itgprofiles.consts import WS_HOST, WS_PORT


async def set_profile(url, player_index, profile_index):
    async with websockets.connect(url) as websocket:
        message = f"{player_index}:{profile_index}"
        await websocket.send(message)
        print(f"Sent message: {message}")


def _get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--server", default=f"ws://{WS_HOST}:{WS_PORT}", help="ProfileSwitcher server URI")
    parser.add_argument("player_number", choices=(0, 1), type=int, help="Target player number")
    parser.add_argument("profile_index", type=int, help="Profile index to load")

    return parser


def main():
    parser = _get_parser()
    args = parser.parse_args()
    asyncio.run(set_profile(args.server, args.player_number, args.profile_index))


if __name__ == "__main__":
    main()
