#!/usr/bin/env python3

# Console Details
ip = "localhost"
port = 49280

# Imports
import socket
import time
import sys
import getopt

def setLevel(socket, dca, level):
    level = int(level)
    socket.sendall("set MIXER:Current/DcaCh/Fader/Level {0} 0 {1}\n".format(dca, level).encode())

def main(ip, port, dca, targetLevel, steps, duration):
    # Console DCA numbers start at 0
    dca = dca - 1

    # Set socket details
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to console
    s.connect((ip,port))

    # Get current level
    s.sendall("get MIXER:Current/DcaCh/Fader/Level {0} 0\n".format(dca).encode())
    response = s.recv(1500).decode().rsplit(" ", 1)

    expectedRespnonsePrefix = "OK get MIXER:Current/DcaCh/Fader/Level {0} 0".format(dca)

    # Check if received expected response
    if response[0] != expectedRespnonsePrefix:
        print("The console did not send back the expected response.")

    startingLevel = int(response[1][:-1].strip('"'))

    # The TF-Rack sets -inf to be -37986.  In reality it's at -14000
    if startingLevel < -14000:
        startingLevel = -14000

    # Remove 0.5s for processing time
    duration = duration * 0.95

    # Fade, if needed
    if duration > 0:
        # Calculate required level differences
        targetLevel = targetLevel * 100 # -3db = -300
        volSpan = targetLevel - startingLevel
        volDelta = volSpan/steps

        currentLevel = startingLevel
        step = 0

        # Remove two steps to avoid overshooting
        while step <= (steps - 2):
            currentLevel = currentLevel + volDelta
            setLevel(s, dca, currentLevel)
            time.sleep((duration)/steps)
            step = step + 1

    # Force set to final level
    setLevel(s, dca, targetLevel)

    # Close socket
    s.close ()

if __name__ == "__main__":
    # Get command line arguments
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv,"d:l:t:")
    except getopt.GetoptError:
        print('USAGE:  fade.py -d <dca> -l <level> -t <fadetime>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-l': # Level
            targetLevel = int(arg)
        elif opt == '-t': # Time
            duration = float(arg)
        elif opt == '-d': # DCA
            dca = int(arg)

    if duration < 0:
        print(f'Fade time cannot be less than 0. ({duration})')
        sys.exit(2)

    # Calculate steps for nice fade
    if duration >= 60:
        steps = int(duration * 10)
    elif duration >= 30:
        steps = int(duration * 50)
    else:
        steps = int(duration * 100)

    print(f'IP:               {ip}')
    print(f'Port:             {port}')
    print(f'DCA:              {dca}')
    print(f'Target Level:     {targetLevel}')
    print(f'Target Duration:  {duration}')
    print(f'Steps:            {steps}')

    startTime = time.perf_counter()
    print(f'Start Time:       {startTime}')

    main(ip, port, dca, targetLevel, steps, duration)

    endTime = time.perf_counter()
    print(f'End Time:         {endTime}')

    print(f'Duration:         {endTime - startTime:0.4f} seconds')
