import socket
import sys

# Set up a TCP/IP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to server address and port 81
server_address = ("localhost", 49280)
tcp_socket.bind(server_address)

# Listen on port 81
tcp_socket.listen(1)

while True:
    print("Waiting for connection")
    connection, client = tcp_socket.accept()

    try:
        print("Connected to client IP: {}".format(client))

        # Receive and print data 1500 bytes at a time, as long as the client is sending something
        while True:
            data = connection.recv(1500).decode().replace("\n", "")
            print(data)

            # Return current level for DCA 1
            if data.startswith("get MIXER:Current/DcaCh/Fader/Level"):
                response = f"OK {data} -13000\n".encode()
                connection.send(response)

            # Set level for DCA 1
            if data.startswith("set MIXER:Current/DcaCh/Fader/Level"):
                response = f"OK {data}".encode()
                connection.send(response)

            if not data:
                break

    except ConnectionResetError as error:
        pass

    except BrokenPipeError as error:
        pass

    finally:
        connection.close()
