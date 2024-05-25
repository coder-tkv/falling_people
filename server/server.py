import socket
from threading import Thread
import pickle

SERVER_HOST = 'localhost'
SERVER_PORT = 4578


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client_sockets = []
        self.server = socket.socket()
        self.server.bind((self.ip, self.port))
        self.server.listen(0)
        print(f'[*] Listening as {self.ip}:{self.port}')
        self.connect_handler()

    def connect_handler(self):
        while True:
            client, address = self.server.accept()
            if client not in self.client_sockets:
                self.client_sockets.append(client)
                name = client.recv(1024)
                pickle_dec = pickle.loads(name)
                if pickle_dec[0] == 'SEND_NAME':
                    name = pickle_dec[1]
                    print(f'{address}, {name} - Successful connection!')
                    listen_for_client_thread = Thread(target=self.listen_for_client, args=(client, name))
                    listen_for_client_thread.start()
                else:
                    self.client_sockets.remove(client)
                    client.close()
                    break

    def sendall(self, current_socket, message):
        for client in self.client_sockets:
            if client != current_socket:
                client.send(message)

    def listen_for_client(self, client: socket.socket, name: str):
        while True:
            try:
                message = client.recv(1024)
                pickle_dec = pickle.loads(message)
                print(f'[!] {name}: {pickle_dec}')
            except Exception as e:
                self.client_sockets.remove(client)
                print(f'[E] {e}')
                break

            if pickle_dec[0] == 'EXIT':
                print(f'[-] {client.getsockname()} - {name}, disconnected.')
                self.client_sockets.remove(client)
                break
            elif pickle_dec[0] == 'SEND_DETECTED' or pickle_dec[0] == 'SEND_UNDETECTED':
                self.sendall(client, message)


if __name__ == '__main__':
    server = Server(SERVER_HOST, SERVER_PORT)
