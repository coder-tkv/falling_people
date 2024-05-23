import socket
from threading import Thread

SERVER_HOST = 'localhost'
SERVER_PORT = 4578

client_sockets = {}
server = socket.socket()
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(5)
print(f'[*] Listening as {SERVER_HOST}:{SERVER_PORT}')


def listen_for_client(cs: socket.socket, ca: tuple, name: str):
    while True:
        try:
            message = cs.recv(1024).decode()
            if not message:
                break
            for el in client_sockets:
                el.sendall(f'[!] {name}: {message}'.encode('utf-8'))
            print(f'[!] {name}: {message}')
        except WindowsError:
            client_sockets.pop(cs)
            break
        except Exception as e:
            print(f'[E] {e}')
    print(f'[-] {ca} - {name}, disconnected.')


if __name__ == '__main__':
    while True:
        client_socket, client_address = server.accept()
        received_name = str(client_socket.recv(1024).decode())
        print(f'[+] {client_address} - {received_name}, connected.')
        client_sockets[client_socket] = received_name
        t = Thread(target=listen_for_client, args=(client_socket, client_address, received_name))
        t.daemon = True
        t.start()
