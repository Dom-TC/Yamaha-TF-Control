#!/usr/bin/env python3

# Console Details
ip = "localhost"
port = 49280

# Imports
import socket
import time
import sys
import getopt

# Sends the command to set a level to a given device
def setLevel(socket, dca, level):
    level = int(level)
    socket.sendall("set MIXER:Current/DcaCh/Fader/Level {0} 0 {1}\n".format(dca, level).encode())

def fadeDCA(socket, dca, targetLevel, duration):
    # Console DCA numbers start at 0
    dca = dca - 1

    # Calculate steps for nice fade
    if duration >= 60:
        steps = int(duration * 10)
    elif duration >= 30:
        steps = int(duration * 50)
    else:
        steps = int(duration * 100)

    # Get current level
    socket.sendall("get MIXER:Current/DcaCh/Fader/Level {0} 0\n".format(dca).encode())
    response = socket.recv(1500).decode().rsplit(" ", 1)

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
        while step <= (steps - 1):
            currentLevel = currentLevel + volDelta
            setLevel(socket, dca, currentLevel)
            time.sleep(duration/steps)
            step = step + 1

    # Force set to final level, in case of overshoot
    setLevel(socket, dca, targetLevel)

if __name__ == "__main__":
    # Get command line arguments
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv,"d:l:t:")
    except getopt.GetoptError:
        print('USAGE:  fade.py -d <dca> -l <level> -t <fadetime>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-d': # DCA
            dca = int(arg)
        elif opt == '-l': # Level
            targetLevel = int(arg)
        elif opt == '-t': # Time
            duration = float(arg)
   
    # We can't fade in negative time...
    if duration < 0:
        print(f'Fade time cannot be less than 0. ({duration})')
        sys.exit(2)

    print(f'IP:               {ip}')
    print(f'Port:             {port}')
    print(f'DCA:              {dca}')
    print(f'Target Level:     {targetLevel}')
    print(f'Target Duration:  {duration}')

     # Set socket details
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to console
    sock.connect((ip,port))

    startTime = time.perf_counter()
    print(f'Start Time:       {startTime}')

    fadeDCA(sock, dca, targetLevel, duration)

    endTime = time.perf_counter()
    print(f'End Time:         {endTime}')

    print(f'Duration:         {endTime - startTime:0.4f} seconds')

    # Close socket
    sock.close ()
