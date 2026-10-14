import socket
import sys


MAX_SIZE = 4096
END_MARKER = "<END>"


def receive_reply(client_socket):
    full_reply = ""

    while END_MARKER not in full_reply:
        piece = client_socket.recv(MAX_SIZE)

        if not piece:
            return ""

        full_reply += piece.decode("utf-8")

    full_reply = full_reply.replace(END_MARKER, "")
    return full_reply


def main():
    if len(sys.argv) != 3:
        print("Usage: py client.py <server_ip> <port>")
        exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, port))
        print("Connected to server")
    except socket.error as error:
        print("connect() failed:", error)
        exit(1)

    while True:
        word = input("Please enter the word that you need defined: ")

        client_socket.sendall(word.encode("utf-8"))

        reply = receive_reply(client_socket)

        if reply == "":
            print("Server closed the connection.")
            break

        print("The Server replied:", reply)

    client_socket.close()


if __name__ == "__main__":
    main()