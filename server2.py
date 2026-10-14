import json
import os
import socket
import sys


# Server2 uses fork so that more than one client can be handled at the same time.
DICTIONARY_FILE = os.path.join("dictionary", "dictionary.json")
MAX_SIZE = 4096
# I added an end marker in the code so that the user knows when the full reply is given. While testing server2, I noticed that the TCP sends a stream of bytes and not seperate messages.
END_MARKER = "<END>"


def load_dictionary():
    try:
        with open(DICTIONARY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Dictionary file was not found.")
        print("Expected path:", DICTIONARY_FILE)
        exit(1)
    except json.JSONDecodeError:
        print("Dictionary file could not be read as JSON.")
        exit(1)


def get_definition(dictionary, word):
    word = word.strip().lower()

    if word == "":
        return "Please enter a word."

    if word in dictionary:
        return dictionary[word]

    return "Word not found in dictionary."


def handle_client(client_socket, dictionary):
    print("Child process is handling a client.")

    while True:
        data = client_socket.recv(MAX_SIZE)

        if not data:
            print("Client disconnected.")
            break

        word = data.decode("utf-8").strip()
        print("Client sent:", word)

        reply = get_definition(dictionary, word)
        client_socket.sendall((reply + END_MARKER).encode("utf-8"))

    client_socket.close()


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 server2.py <port>")
        exit(1)

    port = int(sys.argv[1])
    dictionary = load_dictionary()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)

    print("Server2 is now running on port", port)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from", client_address)

        pid = os.fork()

        if pid == 0:
            # Child process handles this client.
            server_socket.close()
            handle_client(client_socket, dictionary)
            exit(0)
        else:
            # Parent process closes its copy and waits for more clients.
            client_socket.close()


if __name__ == "__main__":
    main()