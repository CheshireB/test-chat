import sys
import socket
import select
import time


from conf import (
    # HOST,
    # PORT,
    ERROR_MESSAGE,
    SUCCESS_MESSAGE,
    RECV_BUFFER,
    LOGIN_HASH,
    DROP_HASH
)

# Все сокеты
SOCKET_LIST = []
# Сокеты, которым можно отправлять сообщения
SOCKET_LIST_LISTENER = []
# Сопоставление сокета и логина
CONNECTION_LOGIN_DICT = {}


def chat_server():

    HOST = input('Input host(example 127.0.0.1):')
    PORT = int(input('Input port(example 8000):'))

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))

    server_socket.listen(2)

    SOCKET_LIST.append(server_socket)

    print("Chat server started on port " + str(PORT))

    while True:
        readers, _, _ = select.select(SOCKET_LIST, [], [], 1)
        for reader in readers:

            # Новое подключение
            if reader == server_socket:
                connection, address = server_socket.accept()
                SOCKET_LIST.append(connection)
                print('SYSTEM LOG - %s - User %s:%s connected to server' % (time.asctime(), address[0], address[1]))

            # Обработка зарегистрированного подключения
            else:

                try:
                    data = reader.recv(RECV_BUFFER).decode()

                    # Проверка на тип сообщения. Если присутствует хэш, то это настройка имени пользователя
                    if data[:len(LOGIN_HASH)] == LOGIN_HASH:
                        login = data[len(LOGIN_HASH):]

                        # Если нет имени
                        if not login:
                            raise ConnectionError

                        # Если такое имя уже присутствует в чате
                        elif login in CONNECTION_LOGIN_DICT.values():
                            message = 'Your login %s is busy' % login
                            reader.send(message.encode())

                        # Если имя написано корректно
                        else:
                            SOCKET_LIST_LISTENER.append(reader)
                            CONNECTION_LOGIN_DICT[reader] = login
                            reader.send(SUCCESS_MESSAGE)
                            message = '%s connected to chat' % login
                            print('SYSTEM LOG - %s - %s' % (time.asctime(), message.strip()))

                    # Проверка от клиента на то, что сервер работает
                    elif data == DROP_HASH:
                        pass

                    # Стандартное сообщение
                    else:
                        login = CONNECTION_LOGIN_DICT[reader]
                        message = '[%s] %s' % (login, data)

                        message_to_all(server_socket, reader, message.encode())
                        print('SYSTEM LOG - %s - %s' % (time.asctime(),message.strip()))

                except:
                    SOCKET_LIST.pop(SOCKET_LIST.index(reader))
                    if reader in CONNECTION_LOGIN_DICT.keys():
                        CONNECTION_LOGIN_DICT.pop(reader)


def message_to_all(server_socket, reader, message):
    for sock in SOCKET_LIST:
        if sock not in [server_socket, reader] and sock in SOCKET_LIST_LISTENER:
            sock.send(message)
    reader.send(SUCCESS_MESSAGE)


if __name__ == "__main__":
    try:
        sys.exit(chat_server())
    except:
        print('Ooops, something went wrong!')