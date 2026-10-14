import json
import os
import socket
import sys

# server1.py will load the dictionary json file first then create a TCP socket and bind it to the port from the command file

DICTIONARY_FILE = os.path.join("dictionary", "dictionary.json")
MAX_SIZE = 4096

# TCP is a byte stream, so the end marker shows where the server response finishes.
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
    print("Connected with client.")

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

# This will create the TCP socket and attach it to the port from the command line. 

def main():
    if len(sys.argv) != 2:
        print("Usage: py server1.py <port>")
        exit(1)

    port = int(sys.argv[1])
    dictionary = load_dictionary()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(1)

    print("Server1 is now running on port", port)

# This will stay working with the client until it disconnects
    while True:
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from", client_address)
        handle_client(client_socket, dictionary)


if __name__ == "__main__":
    main()