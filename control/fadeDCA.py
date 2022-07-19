#!/usr/bin/env python3

# Imports
import argparse
import logging
import socket
import sys
import time

# Console Details
ip = "localhost"
port = 49280

# Version
version = "1.1"
tf_version = "4.01"


# Sends the command to set a level to a given device
def _set_level(socket, dca, level):
    level = int(level)
    socket.sendall(f"set MIXER:Current/DcaCh/Fader/Level {dca} 0 {level}\n".encode())


def fade_dca(socket, dca, target_level, duration):
    # Console DCA numbers start at 0
    dca = dca - 1

    # Adjust duration to deal with processing / response time
    # Calculate steps for nice fade
    duration_multiplier = 1.00
    steps_multiplier = 100
    if duration >= 60:
        duration_multiplier = 1.01
        steps_multiplier = 10
    elif duration >= 30:
        duration_multiplier = 0.97
        steps_multiplier = 50
    else:
        duration_multiplier = 0.96
        steps_multiplier = 100

    duration = duration * duration_multiplier
    steps = int(duration * steps_multiplier)

    # Get current level
    socket.sendall(f"get MIXER:Current/DcaCh/Fader/Level {dca} 0\n".encode())
    response = socket.recv(1500).decode().rsplit(" ", 1)

    expected_respnonse_prefix = f"OK get MIXER:Current/DcaCh/Fader/Level {dca} 0"

    # Check if received expected response
    if response[0] != expected_respnonse_prefix:
        logging.error("The console did not send back the expected response.")
        sys.exit(2)

    # Parse response from console for the final number - the current level
    starting_level = int(response[1][:-1].strip('"'))

    # The TF-Rack sets -inf to be -37986. In reality it's at -14000
    if starting_level < -14000:
        starting_level = -14000

    # Adjust duration to deal with processing / response time
    duration = duration * 0.95

    # Fade, if needed
    if duration > 0:
        # Calculate required level differences
        target_level = target_level * 100  # -3db = -300
        vol_span = target_level - starting_level
        vol_delta = vol_span / steps

        current_level = starting_level
        step = 0

        while step < steps:
            current_level = current_level + vol_delta
            _set_level(socket, dca, current_level)
            time.sleep(duration / steps)
            step = step + 1

    # Force set to final level, to be sure fade ends at exact value
    _set_level(socket, dca, target_level)


if __name__ == "__main__":
    # Set logging config
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Process args
    dca = args.dca
    target_level = args.level
    duration = args.time

    if duration < 0:
        parser.error(f"argument -t/--time: time must be greater than 0: {duration}")

    logging.info(f"IP:               {ip}")
    logging.info(f"Port:             {port}")
    logging.info(f"DCA:              {dca}")
    logging.info(f"Target Level:     {target_level}")
    logging.info(f"Target Duration:  {duration}")

    # Set socket details
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to console
    sock.connect((ip, port))

    # Record the current (start) time to calculate the actual duration at end
    start_time = time.perf_counter()
    logging.info(f"Start Time:       {start_time}")

    fade_dca(sock, dca, target_level, duration)

    # Record the current (end) time
    end_time = time.perf_counter()
    logging.info(f"End Time:         {end_time}")

    # Calculate how long the fade took
    logging.info(f"Duration:         {end_time - start_time:0.4f} seconds")

    # Close socket
    sock.close()
