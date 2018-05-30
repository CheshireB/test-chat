import socket
import sys
import select
import time


from conf import (
    # HOST,
    # PORT,
    RECV_BUFFER,
    MESSAGE,
    ERROR_MESSAGE,
    SUCCESS_MESSAGE,
    LOGIN_HASH,
    DROP_HASH
)


def client():
    try:
        HOST = input('Input host(example 127.0.0.1):')
        PORT = int(input('Input port(example 8000):'))

        connection = socket.socket()
        connection.connect((HOST, PORT))

        print('Connected to server %s:%s' % (HOST, PORT))

        # Получение логина
        while True:
            login = input('Choose your login(not blank): ')

            connection.send((LOGIN_HASH + login).encode())

            # Ожидание ответа от сервера
            start_time = time.time()
            while True:
                message = connection.recv(RECV_BUFFER)
                if message:
                    break

                elif abs(start_time-time.time()) > 5:
                    raise TimeoutError

            if message == SUCCESS_MESSAGE:
                print('SYSTEM - login in SUCCES')
                break

        while True:
            readers, _, _ = select.select([sys.stdin, connection], [], [], 1)

            for reader in readers:

                if reader is connection:
                    reader.settimeout(5)
                    data = connection.recv(RECV_BUFFER)

                    # Отображения сообщения о удачной доставке
                    if data in (SUCCESS_MESSAGE, ERROR_MESSAGE):
                        message = data[len(MESSAGE):].decode()
                        print('SYSTEM - message %s delivered' % message)
                        break

                    # Если приходят пустые сообщения, проверка на то, что сервер работает
                    elif not data:
                        reader.send(DROP_HASH)

                else:
                    message = sys.stdin.readline()
                    connection.send(message.encode())

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    try:
        sys.exit(client())
    except:
        print('PORT\HOST incorrect or server is down!')