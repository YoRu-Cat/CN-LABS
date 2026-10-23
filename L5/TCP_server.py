import socket

HOST = 'localhost'
PORT = 10000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server started on {HOST}:{PORT}, waiting for clients...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    data = conn.recv(1024).decode()
    print(f"Received: {data}")

    # Extract the client ID (last character/word of the message)
    client_id = data.strip()[-1]

    response = f"Hello I am server. Your received ID is {client_id}"
    conn.send(response.encode())
    print(f"Sent: {response}")

    conn.close()   # close this client, then loop back to accept the next one