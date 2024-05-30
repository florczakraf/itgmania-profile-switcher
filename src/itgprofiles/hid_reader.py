import argparse
from pathlib import Path

import evdev

from itgprofiles.consts import WS_HOST, WS_PORT
from itgprofiles.lib import load_mapping, set_player_profile


EVDEV_KEY_MAPPING = {
    evdev.ecodes.KEY_1: "1",
    evdev.ecodes.KEY_2: "2",
    evdev.ecodes.KEY_3: "3",
    evdev.ecodes.KEY_4: "4",
    evdev.ecodes.KEY_5: "5",
    evdev.ecodes.KEY_6: "6",
    evdev.ecodes.KEY_7: "7",
    evdev.ecodes.KEY_8: "8",
    evdev.ecodes.KEY_9: "9",
    evdev.ecodes.KEY_0: "0",
}

def _get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--server", default=f"ws://{WS_HOST}:{WS_PORT}", help="ProfileSwitcher server URI")

    parser.add_argument("--db", required=True, type=Path, help="Path to the database with cards to profiles mapping")
    parser.add_argument("--device", required=True, help="Path to the HID device. Stable paths from /dev/input/by-id/... are recommended")

    parser.add_argument("player_number", choices=(0, 1), type=int, help="Target player number")

    return parser


def main():
    parser = _get_parser()
    args = parser.parse_args()
    mapping = load_mapping(args.db)

    device = evdev.InputDevice(args.device)
    device.grab()

    buffer = ""

    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY and event.value == evdev.events.KeyEvent.key_down:
                if event.code == evdev.ecodes.KEY_ENTER:
                    profile = mapping[buffer]
                    set_player_profile(args.server, args.player_number, profile)
                    buffer = ""
                else:
                    key = EVDEV_KEY_MAPPING[event.code]
                    buffer += key
    finally:
        device.ungrab()
        device.close()
