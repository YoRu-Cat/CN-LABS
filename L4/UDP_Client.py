import socket

def main():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('127.0.0.1', 2000)

    try:
        # Get the request from the user
        # Expected format: YY-AAAA-BR (borrow) or YY-AAAA-RT (return)
        client_message = input("Enter request: ")

        # Send the request to the server
        sock.sendto(client_message.encode(), server_address)

        # Receive the response from the server
        server_message, _ = sock.recvfrom(2000)
        print(server_message.decode())

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the socket
        sock.close()

if __name__ == "__main__":
    main()
