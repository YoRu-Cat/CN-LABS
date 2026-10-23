import socket

HOST = 'localhost'
PORT = 10000

client_id = input("Enter your ID (0-9): ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

message = f"Hello I am client and My ID is {client_id}"
client_socket.send(message.encode())
print(f"Sent: {message}")

response = client_socket.recv(1024).decode()
print(f"Received: {response}")

client_socket.close()