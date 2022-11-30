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


def recall_scene(socket, bank, scene):
    bank = bank.lower()

    # Validate scene
    if type(scene) != int or scene not in range(0, 100):
        logging.error(f"Scene must be a number between 1 and 99: {scene}")
        sys.exit(2)

    # Validate bank
    if bank != "a" and bank != "b":
        logging.error(f"Bank must be either `a` or `b`: {bank}")
        sys.exit(2)

    # Recall scene
    logging.info(f"Recalling: {bank.upper()}{scene}")
    socket.sendall(f"ssrecall_ex scene_{bank} {scene}\n".encode())

    # Confirm expected response
    response = socket.recv(1500).decode()
    expected_response = f"OK ssrecall_ex scene_{bank} {scene}"

    if response.strip() != expected_response.strip():
        logging.error(
            f"The console did not send back the expected response.\nExpected:   {expected_response}\nRecieved:   {response}"
        )


if __name__ == "__main__":
    # Set logging config
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Create argparser
    parser = argparse.ArgumentParser(
        prog="recall_scene",
        description="Recall a scene on a Yamaha TF-series sound console.",
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

    # Bank letter
    parser.add_argument(
        "-b",
        "--bank",
        metavar="<bank>",
        type=str,
        default="a",
        help="the scene bank",
        choices=["a", "b"],
    )

    # Scene number
    parser.add_argument(
        "-s",
        "--scene",
        metavar="<scene>",
        type=int,
        required=True,
        help="the scene to recall",
        choices=range(0, 100),
    )

    # Process args
    args = parser.parse_args()
    bank = args.bank
    scene = args.scene

    logging.info(f"IP:        {ip}")
    logging.info(f"Port:      {port}")
    logging.info(f"Bank:      {bank}")
    logging.info(f"Scene:     {scene}")

    # Set socket details
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to console
    sock.connect((ip, port))

    recall_scene(sock, bank, scene)

    # Close socket
    sock.close()
