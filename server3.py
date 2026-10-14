import json
import os
import select
import socket
import sys

# server3 keeps the main server socket and all client sockets in one list. select() checks which sockets are ready. 
# If the ready socket is the server socket, that means a new client is connecting. 
# If the ready socket is a client socket, that means the client sent a word, so the server reads it, looks up the definition, and sends the reply back.


# Server3 uses select() so one process can watch multiple client sockets.
# Select tells the server which sockets are ready to be read from.

DICTIONARY_FILE = os.path.join("dictionary", "dictionary.json")
MAX_SIZE = 4096

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


def main():
    if len(sys.argv) != 2:
        print("Usage: py server3.py <port>")
        exit(1)

    port = int(sys.argv[1])
    dictionary = load_dictionary()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)

    # This list keeps track of the server socket and all of the connected clients.
    
    socket_list = [server_socket]

    print("Server3 is now running on port", port)

    while True:
        readable_sockets, _, error_sockets = select.select(socket_list, [], socket_list)

        for current_socket in readable_sockets:
            if current_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                socket_list.append(client_socket)
                print("Accepted connection from", client_address)
            else:
                data = current_socket.recv(MAX_SIZE)

                if not data:
                    print("Client disconnected.")
                    socket_list.remove(current_socket)
                    current_socket.close()
                else:
                    word = data.decode("utf-8").strip()
                    print("Client sent:", word)

                    reply = get_definition(dictionary, word)
                    current_socket.sendall((reply + END_MARKER).encode("utf-8"))

        for bad_socket in error_sockets:
            if bad_socket in socket_list:
                socket_list.remove(bad_socket)
            bad_socket.close()


if __name__ == "__main__":
    main()