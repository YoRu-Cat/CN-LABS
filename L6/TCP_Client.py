import socket


def main():
    server_ip = '127.0.0.1'
    server_port = 2000
    buffer_size = 2000

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")
    except socket.error as err:
        print(f"Could not create socket. Error: {err}")
        return

    try:
        client_socket.connect((server_ip, server_port))
        print("Connected to server")
    except socket.error as err:
        print(f"Connection failed. Error: {err}")
        return

    while True:
        server_message = client_socket.recv(buffer_size).decode()
        if server_message == "":
            break

        if server_message.endswith(": "):
            answer = input(server_message)
            client_socket.send(answer.encode())
        else:
            print(server_message)
            break

    client_socket.close()


if __name__ == "__main__":
    main()
