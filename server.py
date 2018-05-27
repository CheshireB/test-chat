import sys
import socket
import select


HOST = '127.0.0.1'
RECV_BUFFER = 1024
PORT = 8000

SOCKET_LIST = []


def chat_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))

    server_socket.listen(2)

    SOCKET_LIST.append(server_socket)

    print("Chat server started on port " + str(PORT))

    while True:
        for sock in SOCKET_LIST:
            readers, _,_ = select.select()

            if sock == server_socket:
                connection, address = server_socket.accept()
                SOCKET_LIST.append(connection)

                print('Log: client (%s, %s) connected' % address)

                message_to_all(server_socket, sock, "User %s:%s entered to chat" % address)

            else:
                data = sock.recv(RECV_BUFFER)
                if data.decode() == 'quit':
                    break


def message_to_all(server_socket, own_socket, message):
    for sock in SOCKET_LIST:
        if sock != server_socket and sock != own_socket:
            sock.send(message.encode())


if __name__ == "__main__":
    sys.exit(chat_server())