import socket

HOST = 'localhost'
PORT = 10001

def has_vowel(word):
    return any(ch.lower() in 'aeiou' for ch in word)

def process_sentence(sentence):
    words = sentence.split(' ')
    result = []
    for word in words:
        if has_vowel(word):
            result.append(word[::-1])
        else:
            result.append(word)
    return ' '.join(result)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server started on {HOST}:{PORT}, waiting for clients...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    data = conn.recv(4096).decode()
    print(f"Received sentence: {data}")

    processed = process_sentence(data)
    print(f"Sending back: {processed}")

    conn.send(processed.encode())
    conn.close()