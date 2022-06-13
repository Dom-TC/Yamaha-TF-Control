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
import argparse
import logging

# Sends the command to set a level to a given device
def setLevel(socket, dca, level):
    level = int(level)
    socket.sendall(
        "set MIXER:Current/DcaCh/Fader/Level {0} 0 {1}\n".format(dca, level).encode()
    )


def fadeDCA(socket, dca, targetLevel, duration):
    # Console DCA numbers start at 0
    dca = dca - 1

    # Adjust duration to deal with processing / response time
    # Calculate steps for nice fade
    durationMultiplier = 1.00
    stepsMultiplier = 100
    if duration >= 60:
        durationMultiplier = 1.01
        stepsMultiplier = 10
    elif duration >= 30:
        durationMultiplier = 0.97
        stepsMultiplier = 50
    else:
        durationMultiplier = 0.96
        stepsMultiplier = 100

    duration = duration * durationMultiplier
    steps = int(duration * stepsMultiplier)

    # Get current level
    socket.sendall("get MIXER:Current/DcaCh/Fader/Level {0} 0\n".format(dca).encode())
    response = socket.recv(1500).decode().rsplit(" ", 1)

    expectedRespnonsePrefix = "OK get MIXER:Current/DcaCh/Fader/Level {0} 0".format(dca)

    # Check if received expected response
    if response[0] != expectedRespnonsePrefix:
        logging.error("The console did not send back the expected response.")
        sys.exit(2)

    # Parse response from console for the final number - the current level
    startingLevel = int(response[1][:-1].strip('"'))

    # The TF-Rack sets -inf to be -37986. In reality it's at -14000
    if startingLevel < -14000:
        startingLevel = -14000

    # Adjust duration to deal with processing / response time
    duration = duration * 0.95

    # Fade, if needed
    if duration > 0:
        # Calculate required level differences
        targetLevel = targetLevel * 100  # -3db = -300
        volSpan = targetLevel - startingLevel
        volDelta = volSpan / steps

        currentLevel = startingLevel
        step = 0

        while step < steps:
            currentLevel = currentLevel + volDelta
            setLevel(socket, dca, currentLevel)
            time.sleep(duration / steps)
            step = step + 1

    # Force set to final level, to be sure fade ends at exact value
    setLevel(socket, dca, targetLevel)


if __name__ == "__main__":
    # Set logging config
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Create argparser
    parser = argparse.ArgumentParser(
        prog="fadeDCA",
        description="Fade a DCA on a Yamaha TF-series sound console.",
    )

    # version
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="returns the version number",
        version=f"%(prog)s {version}",
    )

    # DCA number
    parser.add_argument(
        "-d",
        "--dca",
        metavar="<dca>",
        type=int,
        required=True,
        help="the DCA to fade",
        choices=range(1, 9),
    )

    # Target level
    parser.add_argument(
        "-l",
        "--level",
        metavar="<level>",
        type=int,
        required=True,
        help="the target level",
    )

    # Duration
    parser.add_argument(
        "-t",
        "--time",
        metavar="<duration>",
        type=float,
        required=True,
        help="the fade duration",
    )

    # Process args
    args = parser.parse_args()
    dca = args.dca
    targetLevel = args.level
    duration = args.time

    if duration < 0:
        parser.error(f"argument -t/--time: time must be greater than 0: {duration}")

    logging.info(f"IP:               {ip}")
    logging.info(f"Port:             {port}")
    logging.info(f"DCA:              {dca}")
    logging.info(f"Target Level:     {targetLevel}")
    logging.info(f"Target Duration:  {duration}")

    # Set socket details
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to console
    sock.connect((ip, port))

    # Record the current (start) time to calculate the actual duration at end
    startTime = time.perf_counter()
    logging.info(f"Start Time:       {startTime}")

    fadeDCA(sock, dca, targetLevel, duration)

    # Record the current (end) time
    endTime = time.perf_counter()
    logging.info(f"End Time:         {endTime}")

    # Calculate how long the fade took
    logging.info(f"Duration:         {endTime - startTime:0.4f} seconds")

    # Close socket
    sock.close()
