import argparse
from pathlib import Path

from pexpect_serial import SerialSpawn
import serial
import pexpect

from itgprofiles.consts import WS_HOST, WS_PORT
from itgprofiles.lib import load_mapping, set_player_profile

FLIPPER_PROMPT = b">: "
CARD_TYPE = "EM4100"
CTRL_C = b"\x03"


def get_card_id(s: str):
    for line in s.splitlines(keepends=False):
        line = line.strip()
        if line.startswith(CARD_TYPE):
            hex_string = line[-8:]
            return f'{int(hex_string, 16):010}'
    return None


def _get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--server", default=f"ws://{WS_HOST}:{WS_PORT}", help="ProfileSwitcher server URI")
    parser.add_argument("--device", default="/dev/ttyACM0", help="Path to the serial device")
    parser.add_argument("--baud-rate", default=115200, type=int, help="Path to the serial device")

    parser.add_argument("--db", required=True, type=Path, help="Path to the database with cards to profiles mapping")

    parser.add_argument("player_number", choices=(0, 1), type=int, help="Target player number")

    return parser


def main():
    parser = _get_parser()
    args = parser.parse_args()
    mapping = load_mapping(args.db)

    with serial.Serial(args.device, args.baud_rate, timeout=0) as serial_connection:
        ss = SerialSpawn(serial_connection)
        ss.send(CTRL_C)
        ss.expect(FLIPPER_PROMPT)
        print("Staring the rfid read loop")
        while True:
            ss.send(b"rfid read normal\r\n")
            try:
                ss.expect(b"to abort", timeout=1)
                ss.expect(b"Reading stopped", timeout=10)
                result = ss.before.decode()
                card_id = get_card_id(result)
                if card_id:
                    profile = mapping[card_id]
                    set_player_profile(args.server, args.player_number, profile)
            except pexpect.TIMEOUT:
                print(f"Timed-out, resetting reader: {ss.before.decode().strip()}")
                ss.send(CTRL_C)
                ss.expect(FLIPPER_PROMPT)


if __name__ == "__main__":
    main()
