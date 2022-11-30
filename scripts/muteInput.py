#!/usr/bin/env python3

# Imports
import argparse
import logging
import socket
import sys

# Console Details
ip = "localhost"
port = 49280

# Version
version = "1.2"
tf_version = "4.01"


def set_input_mute(socket, channel, state):
    state = state.lower()

    # Validate bank
    if state == "off":
        state_code = 0
    elif state == "on":
        state_code = 1
    else:
        logging.error(f"State must be either `on` or `off`: {state}")
        sys.exit(2)

    # Recall scene
    logging.info(f"Setting channel {channel} mute to {state}")
    socket.sendall(
        f"set MIXER:Current/InCh/Fader/On {channel - 1} 0 {state_code}\n".encode()
    )

    # Confirm expected response
    response = socket.recv(1500).decode()
    expected_response = (
        f"OK set MIXER:Current/InCh/Fader/On {channel - 1} 0 {state_code}"
    )

    if response.strip() != expected_response.strip():
        logging.error(
            f"The console did not send back the expected response.\nExpected:   {expected_response}\nRecieved:   {response}"
        )


if __name__ == "__main__":
    # Set logging config
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Create argparser
    parser = argparse.ArgumentParser(
        prog="set_input_mute",
        description="Sets the state of an input mute on a Yamaha TF-series sound console.",
        epilog=f"These scripts have been tested against a Yamaha TF-Rack v{tf_version}",
    )

    # version
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="returns the version number",
        version=f"%(prog)s v{version}",
    )

    # Channel
    parser.add_argument(
        "-c",
        "--channel",
        metavar="<channel>",
        type=int,
        required=True,
        help="the channel to be muted",
        choices=range(1, 41),
    )

    # State
    parser.add_argument(
        "-s",
        "--state",
        metavar="<state>",
        type=str,
        required=True,
        help="the state to set the channel's mute to",
        choices=["on", "off"],
    )

    # Process args
    args = parser.parse_args()
    channel = args.channel
    state = args.state

    logging.info(f"IP:          {ip}")
    logging.info(f"Port:        {port}")
    logging.info(f"Channel:     {channel}")
    logging.info(f"State:       {state}")

    # Set socket details
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to console
    sock.connect((ip, port))

    set_input_mute(sock, channel, state)

    # Close socket
    sock.close()
