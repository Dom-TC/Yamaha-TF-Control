#!/usr/bin/env python3

# Console Details
ip = "localhost"
port = 49280

# Version
version = "1.1"

# Imports
import socket
import time
import sys
import getopt
import logging


def recallScene(socket, scene):
    # Recall scene
    logging.info(f"Recalling: {scene}")
    socket.sendall("ssrecall_ex scene_a {0}\n".format(scene).encode())

    # Confirm expected response
    response = socket.recv(1500).decode()
    expected_response = f"OK ssrecall_ex scene_a {scene}"

    if response != expected_response:
        logging.error(
            f"The console did not send back the expected response.\nExpected:   {expected_response}\nRecieved:   {response}"
        )


if __name__ == "__main__":
    # Set logging config
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    #  Get command line arguments
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "s:")
    except getopt.GetoptError:
        logging.error("USAGE:  recallScene.py -s <scene number>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-s":  # Level
            scene = int(arg)

    logging.info(f"IP:      {ip}")
    logging.info(f"Port:    {port}")
    logging.info(f"Bank:    {bank}")
    logging.info(f"Scene:   {scene}")

    # Set socket details
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to console
    sock.connect((ip, port))

    recallScene(sock, scene)

    # Close socket
    sock.close()
