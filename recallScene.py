# Imports
import socket
import time
import sys
import getopt


def recallScene(ip, port, scene):
    # Set socket details
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to console
    s.connect((ip, port))

    # Recall scene
    print("Recalling: ", scene)
    s.sendall("ssrecall_ex scene_a {0}\n".format(scene).encode())
    print(s.recv(1500))

    # Close socket
    s.close()


if __name__ == "__main__":
    # Console Details
    ip = "192.168.2.150"
    port = 49280

    scene = 11

    #  Get command line arguments
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "s:")
    except getopt.GetoptError:
        print("USAGE:  recallScene.py -s <scene number>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-s":  # Level
            scene = int(arg)

    recallScene(ip, port, scene)
