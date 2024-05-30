import asyncio
import evdev

import websockets

player = "0"
address = "ws://localhost:5555"
input_device = "/dev/input/by-id/usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd"

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

device = evdev.InputDevice(input_device)
device.grab()

buffer = ""

try:
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY and event.value == evdev.events.KeyEvent.key_down:
            if event.code == evdev.ecodes.KEY_ENTER:
                profile = mapping[buffer]
                print(f"picking profile {profile}")
                run_websocket_client(address, f"{player}:{profile}")
                buffer = ""
            else:
                key = keys[event.code]
                buffer += key
finally:
    device.ungrab()
    device.close()