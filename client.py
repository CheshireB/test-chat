import socket
import sys
import select

def Main():
    host = '127.0.0.1'
    port = 8000

    connection = socket.socket()
    connection.connect((host, port))

    print('Connected to server %s:%s' % (host, port))


    while True:
        readers, _, _ = select.select([sys.stdin, connection], [], [], 1)

        for reader in readers:
            if reader is connection:
                data = connection.recv(1024).decode()
                print(data)
            else:
                message = sys.stdin.readline()
                connection.send(message.encode())
                sys.stdout.write('[Me] ')
                sys.stdout.flush()

if __name__ == '__main__':
    sys.exit(Main())