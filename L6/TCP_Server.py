import socket
import threading
import re
import os

host = '127.0.0.1'
port = 2000
buffer_size = 2000

lock = threading.Lock()
voted = []


def read_voters():
    voters = []
    file = open("Voters_List.txt", "r")
    for line in file:
        line = line.strip()
        if line != "":
            voters.append(line.split("/"))
    file.close()
    return voters


def read_candidates():
    candidates = []
    file = open("Candidates_List.txt", "r")
    for line in file:
        line = line.strip()
        if line != "":
            candidates.append(re.split(r"\t|\s{2,}", line))
    file.close()
    return candidates


def read_old_votes():
    if os.path.exists("Votes.txt"):
        file = open("Votes.txt", "r")
        for line in file:
            parts = line.strip().split("/")
            if len(parts) == 3:
                voted.append(parts[1])
        file.close()


def handle_client(client_socket):
    voters = read_voters()
    candidates = read_candidates()

    client_socket.send("Enter Name: ".encode())
    name = client_socket.recv(buffer_size).decode().strip()

    client_socket.send("Enter CNIC: ".encode())
    cnic = client_socket.recv(buffer_size).decode().strip()

    found = False
    for voter in voters:
        if voter[0] == name and voter[1] == cnic:
            found = True

    if found == False:
        client_socket.send("Authentication failed. You are not a registered voter.".encode())
        client_socket.close()
        return

    if cnic in voted:
        client_socket.send("You have already cast your vote. You cannot vote again.".encode())
        client_socket.close()
        return

    message = "Authentication successful.\n"
    message = message + "Welcome, " + name + ".\n"
    message = message + "Available Candidates:\n"
    for candidate in candidates:
        message = message + candidate[0] + " - " + candidate[1] + "\n"
    message = message + "Enter poll symbol: "
    client_socket.send(message.encode())

    while True:
        symbol = client_socket.recv(buffer_size).decode().strip()

        valid = False
        for candidate in candidates:
            if candidate[1] == symbol:
                valid = True

        if valid == False:
            client_socket.send("Invalid poll symbol. Please enter a valid poll symbol.\nEnter poll symbol: ".encode())
        else:
            break

    lock.acquire()
    if cnic in voted:
        lock.release()
        client_socket.send("You have already cast your vote. You cannot vote again.".encode())
    else:
        voted.append(cnic)
        file = open("Votes.txt", "a")
        file.write(name + "/" + cnic + "/" + symbol + "\n")
        file.close()
        lock.release()
        client_socket.send("Vote recorded successfully.".encode())

    client_socket.close()


def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")
    except socket.error as err:
        print(f"Could not create socket. Error: {err}")
        return

    try:
        server_socket.bind((host, port))
        print("Bind done")
    except socket.error as err:
        print(f"Bind failed. Error: {err}")
        return

    server_socket.listen(10)
    print("Listening for incoming connections...")

    read_old_votes()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connected with IP: {client_address[0]} and Port No: {client_address[1]}")

        t = threading.Thread(target=handle_client, args=(client_socket,))
        t.start()


if __name__ == "__main__":
    main()
