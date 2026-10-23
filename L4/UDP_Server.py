import socket
import re

# Regex to validate request format: YY-AAAA-BR or YY-AAAA-RT
REQUEST_PATTERN = re.compile(r'^\d{2}-\d{4}-(BR|RT)$')

def process_request(request, students):
   
    request = request.strip()

    # Validate format
    if not REQUEST_PATTERN.match(request):
        return "Invalid request format."

    # Split roll number and action (e.g. "24-4159-BR" -> "24-4159", "BR")
    roll_number, action = request.rsplit('-', 1)

    if action == "BR":
        if roll_number in students:
            return "You have already borrowed a book."
        else:
            students.append(roll_number)
            return f"Book issued to Student {roll_number}."

    elif action == "RT":
        if roll_number in students:
            students.remove(roll_number)
            return f"Book returned by Student {roll_number}. Thank you."
        else:
            return "You have not borrowed a book. Contact Library Administrator."


def main():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the server address and port
    server_address = ('127.0.0.1', 2000)
    sock.bind(server_address)

    print("Socket created and bound")
    print("Listening for messages...\n")

    # Library records: list of roll numbers with a currently borrowed book
    students = []

    while True:
        try:
            # Receive the request from the client
            client_message, client_address = sock.recvfrom(2000)
            request = client_message.decode()

            print(f"Received message from IP: {client_address[0]} and Port No: {client_address[1]}")
            print(f"Request received: {request}")

            # Process the request and get the response
            response = process_request(request, students)

            # Send the response back to the client
            sock.sendto(response.encode(), client_address)

            print(response)
            print(f"Current students: {students}\n")

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # Closing the socket
    sock.close()

if __name__ == "__main__":
    main()
