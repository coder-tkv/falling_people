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
    if name == 'client_pc':
        while True:
            try:
                message = cs.recv(1024).decode()
                if not message:
                    break
                print(f'[!] {name}: {message}')
            except WindowsError:
                client_sockets.pop(cs)
                break
            except Exception as e:
                print(f'[!] Error: {e}')
        print(f'[-] {ca} - {name}, disconnected.')
    elif name == 'client_robot':
        while True:
            try:
                message = cs.recv(1024).decode()
                if not message:
                    break
                print(f'[!] {name}: {message}')
            except WindowsError:
                client_sockets.pop(cs)
                break
            except Exception as e:
                print(f'[!] Error: {e}')
        print(f'[-] {ca} - {name}, disconnected. ')
    else:
        print(f'[-] {ca} - {name}, disconnected. The client name is incorrect.')
        cs.close()


while True:
    client_socket, client_address = server.accept()
    received_name = str(client_socket.recv(1024).decode())
    print(f'[+] {client_address} - {received_name}, connected.')
    client_sockets[client_socket] = received_name
    t = Thread(target=listen_for_client, args=(client_socket, client_address, received_name))
    t.daemon = True
    t.start()
