#!/usr/bin/env python3

# Console Details
ip = "localhost"
port = 49280

# Version
version = "1.0"
tf_version = "4.2"

# Imports
import socket
import sys
import argparse
import logging


def setMuteMaster(socket, master, state):
    master = master.lower()
    state = state.lower()

    # Get master code
    if master == "input":
        masterCode = 0
    elif master == "fx":
        masterCode = 1
    else:
        logging.error(f"Master must be either `input` or `fx`: {master}")
        sys.exit(2)

    # Validate bank
    if state == "off":
        stateCode = 0
    elif state == "on":
        stateCode = 1
    else:
        logging.error(f"State must be either `on` or `off`: {state}")
        sys.exit(2)

    # Recall scene
    logging.info(f"Setting {master} mute to {state}")
    socket.sendall(
        f"set MIXER:Current/MuteMaster/On {masterCode} 0 {stateCode}\n".encode()
    )

    # Confirm expected response
    response = socket.recv(1500).decode()
    expected_response = f"OK set MIXER:Current/MuteMaster/On {masterCode} 0 {stateCode}"

    if response != expected_response:
        logging.error(
            f"The console did not send back the expected response.\nExpected:   {expected_response}\nRecieved:   {response}"
        )


if __name__ == "__main__":
    # Set logging config
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Create argparser
    parser = argparse.ArgumentParser(
        prog="setMuteMaster",
        description="Sets the input and fx mute masters on a Yamaha TF-series sound console.",
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

    # Master
    parser.add_argument(
        "-m",
        "--master",
        metavar="<master>",
        type=str,
        default="input",
        help="the mute master to be set",
        choices=["input", "fx"],
    )

    # State
    parser.add_argument(
        "-s",
        "--state",
        metavar="<state>",
        type=str,
        required=True,
        help="the state to set the mute master to",
        choices=["on", "off"],
    )

    # Process args
    args = parser.parse_args()
    master = args.master
    state = args.state

    logging.info(f"IP:          {ip}")
    logging.info(f"Port:        {port}")
    logging.info(f"Master:      {master}")
    logging.info(f"State:       {state}")

    # Set socket details
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to console
    sock.connect((ip, port))

    setMuteMaster(sock, master, state)

    # Close socket
    sock.close()
