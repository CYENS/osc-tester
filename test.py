import argparse
import re
import time
from typing import Tuple
from pythonosc.udp_client import SimpleUDPClient


def parse_line(line: str) -> Tuple[str, float]:
    """
    Extracts the OSC address and float value from a single log line.
    """
    address_match = re.search(r'ADDRESS\((.*?)\)', line)
    float_match = re.search(r'FLOAT\(([-+]?[0-9]*\.?[0-9]+)\)', line)

    if not address_match or not float_match:
        raise ValueError(f"Invalid line format: {line.strip()}")

    address = address_match.group(1)
    value = float(float_match.group(1))

    return address, value


def send_osc_messages(file_path: str, ip: str, port: int, repeat: bool, fps: float) -> None:
    client = SimpleUDPClient(ip, port)
    delay = 1.0 / fps if fps > 0 else 0.0

    while True:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    address, value = parse_line(line)
                    client.send_message(address, value)
                    # print(f"Sent {address} {value}")
                    # time.sleep(delay)
                except ValueError as e:
                    print(f"Skipping line: {e}")

        if not repeat:
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="Send OSC messages from a log file.")
    parser.add_argument("file", type=str, help="Path to the input file.")
    parser.add_argument("--send-ip", type=str, default="127.0.0.1", help="Destination IP address.")
    parser.add_argument("--send-port", type=int, default=52071, help="Destination port number.")
    parser.add_argument("--repeat", action="store_true", help="Repeat sending messages indefinitely.")
    parser.add_argument("--fps", type=float, default=60.0, help="Frames per second (messages per second).")

    args = parser.parse_args()

    send_osc_messages(args.file, args.send_ip, args.send_port, args.repeat, args.fps)


if __name__ == "__main__":
    main()
