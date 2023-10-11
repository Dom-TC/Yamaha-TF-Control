import socket
import sys

# Set up a TCP/IP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Listen for incoming TCP Connections
server_address = ("localhost", 49280)
tcp_socket.bind(server_address)
tcp_socket.listen(1)

while True:
    print("Waiting for connection")
    connection, client = tcp_socket.accept()

    try:
        print(f"Connected to client IP: {client}")

        # Receive and print data 1500 bytes at a time, as long as the client is sending something
        while True:
            data = connection.recv(1500).decode().replace("\n", "")
            print(data)

            # Get DCA Level
            if data.startswith("get MIXER:Current/DcaCh/Fader/Level"):
                response = f"OK {data} -13000\n".encode()
                connection.send(response)

            # Set DCA Level
            if data.startswith("set MIXER:Current/DcaCh/Fader/Level"):
                response = f"OK {data}".encode()
                connection.send(response)

            # Recall scene
            if data.startswith("ssrecall_ex"):
                response = f"OK {data}".encode()
                connection.send(response)

            # Set mute master
            if data.startswith("set MIXER:Current/MuteMaster/On"):
                mute_state = int(data[-1:])
                if mute_state == 1:
                    suffix = '"ON"'
                elif mute_state == 0:
                    suffix = '"OFF"'

                response = f"OK {data} {suffix}".encode()
                connection.send(response)

            # Set input mute
            if data.startswith("set MIXER:Current/InCh/Fader/On"):
                mute_state = int(data[-1:])
                if mute_state == 1:
                    suffix = '"ON"'
                elif mute_state == 0:
                    suffix = '"OFF"'

                response = f"OK {data} {suffix}".encode()
                connection.send(response)

            if not data:
                break

    except ConnectionResetError:
        pass

    except BrokenPipeError:
        pass

    finally:
        connection.close()
