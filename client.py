import socket


def client(host: str, port: int) -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect((host, port))

    msg = input(">>> ")

    while msg.lower().strip() != ["exit", "quit"]:
        client_socket.send(msg.encode())
        client_socket.recv(1024).decode()

    client_socket.close()
