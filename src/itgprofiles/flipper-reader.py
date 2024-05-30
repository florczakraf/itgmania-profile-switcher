import asyncio
import evdev

import websockets

player = "1"
address = "ws://localhost:5555"
input_device = "/dev/ttyACM0"
CARD_TYPE = "EM4100"

mapping = {
    "0015346786": 0,
    "0015352146": 1,
    "0007038511": 2,
    "0015388888": 3,
    "0007012214": 4,
    "0007080131": 5,
}
keys = {
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

async def websocket_client(uri, message):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        print(f"Sent message: {message}")

def run_websocket_client(uri, message):
    asyncio.run(websocket_client(uri, message))


import serial
from pexpect_serial import SerialSpawn
import pexpect


def get_card_id(s: str):
    for line in s.splitlines(keepends=False):
        line = line.strip()
        if line.startswith(CARD_TYPE):
            hex_string = line[-8:]
            return f'{int(hex_string, 16):010}'
    return None

PROMPT = b">: "
with serial.Serial(input_device, 115200, timeout=0) as serial_connection:
    ss = SerialSpawn(serial_connection)
    ss.send(b"\x03")  # ctrl-c to reset state
    ss.expect(PROMPT)
    print("staring loop")
    while True:
        ss.send(b"rfid read normal\r\n")
        try:
            ss.expect(b"to abort", timeout=1)
            ss.expect(b"Reading stopped", timeout=10)
            result = ss.before.decode()
            card_id = get_card_id(result)
            profile = mapping[card_id]
            print(f"picking profile {profile}")
            run_websocket_client(address, f"{player}:{profile}")
        except pexpect.TIMEOUT:
            print(f"Timed-out, resetting reader: {ss.before.decode()}")
            ss.send(b"\x03")  # ctrl-c to reset state
            ss.expect(PROMPT)
