import socket
from threading import Thread

NAME = 'client_robot'
HOSTNAME = 'localhost'
PORT = 4578
data = NAME

client = socket.socket()
print(f'[*] Connecting to {HOSTNAME}:{PORT} with name {NAME}')
client.connect((HOSTNAME, PORT))
print(f'[+] Connected with name {NAME}.')


def listen_for_messages():
    while True:
        message = client.recv(1024).decode()
        print(message)


if __name__ == '__main__':
    t = Thread(target=listen_for_messages)
    t.daemon = True
    t.start()
    while data != 'stop':
        client.sendall(data.encode('utf-8'))
        data = input()
    print('[-] Disconnected.')
    client.close()
