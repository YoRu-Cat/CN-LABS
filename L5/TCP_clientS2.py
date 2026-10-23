import socket

HOST = 'localhost'
PORT = 10001

def has_vowel(word):
    return any(ch.lower() in 'aeiou' for ch in word)

def process_sentence(sentence):
    words = sentence.split(' ')
    result = []
    for word in words:
        if not has_vowel(word):
            result.append(word[::-1])
        else:
            result.append(word)
    return ' '.join(result)

sentence = input("Enter a sentence: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_socket.send(sentence.encode())

response = client_socket.recv(4096).decode()
print(f"Received from server: {response}")

final_result = process_sentence(response)
print(f"Final sentence: {final_result}")

client_socket.close()