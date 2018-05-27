import sys
import socket
import select
import time


from conf import (
    HOST,
    PORT,
    ERROR_MESSAGE,
    SUCCES_MESSAGE,
    RECV_BUFFER,
)

SOCKET_LIST = []


def chat_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))

    server_socket.listen(2)

    SOCKET_LIST.append(server_socket)

    print("Chat server started on port " + str(PORT))

    while True:
        readers, _, _ = select.select(SOCKET_LIST, [], [], 1)
        for reader in readers:

            if reader == server_socket:
                connection, address = server_socket.accept()
                SOCKET_LIST.append(connection)
                print('SYSTEM LOG - '+time.asctime() + ' - User %s:%s connected to chat'%address)

            else:
                address_string = '[%s:%s]'%reader.getpeername()
                try:
                    data = address_string+' - '+reader.recv(RECV_BUFFER).decode()
                    message_to_all(server_socket, reader, data.encode())
                    print('SYSTEM LOG - ', time.asctime(), ' - ', data.strip())

                except:
                    print('SYSTEM LOG - '+time.asctime() + ' - Problems with ', address_string)
                    reader.send(ERROR_MESSAGE)


def message_to_all(server_socket, reader, message):
    for sock in SOCKET_LIST:
        if sock != server_socket and sock != reader:
            sock.send(message)
    reader.send(SUCCES_MESSAGE)








if __name__ == "__main__":
    sys.exit(chat_server())