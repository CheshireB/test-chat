import socket
import sys
import select


from conf import (
    HOST,
    PORT,
    RECV_BUFFER,
    MESSAGE,
    ERROR_MESSAGE,
    SUCCES_MESSAGE,
    HASH
)


def client():


    connection = socket.socket()
    connection.connect((HOST, PORT))
    print('Connected to server %s:%s' % (HOST, PORT))

    while True:
        login = input('Choose your login(not blank): ')
        connection.send((HASH+login).encode())

        while True:
            message = connection.recv(RECV_BUFFER)
            if message:
                break

        if message == SUCCES_MESSAGE:
            print('SYSTEM - login in SUCCES')
            break

    while True:
        readers, _, _ = select.select([sys.stdin, connection], [], [], 1)

        for reader in readers:

            if reader is connection:
                data = connection.recv(RECV_BUFFER)

                if data in (SUCCES_MESSAGE, ERROR_MESSAGE):
                    message = data[len(MESSAGE):].decode()
                    print('SYSTEM - message %s delivered' % message)
                    break

                print(data.decode())
            else:
                message = sys.stdin.readline()
                connection.send(message.encode())


if __name__ == '__main__':
    sys.exit(client())
