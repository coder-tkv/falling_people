import socket
from threading import Thread
import pickle

SERVER_HOST = 'localhost'
SERVER_PORT = 4578
NAME = 'client_robot'


class Client:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name
        self.client = socket.socket()
        print(f'[*] Connecting to {self.ip}:{self.port} with name {self.name}')
        self.client.connect((self.ip, self.port))
        print(f'[+] Connected with name {self.name}.')
        payload = ['SEND_NAME', f"{self.name}"]
        self.send_message(payload)
        listen_for_messages_thread = Thread(target=self.listen_for_messages)
        listen_for_messages_thread.start()

    def listen_for_messages(self):
        while True:
            try:
                message = self.client.recv(1024)
            except OSError:
                return
            pickle_dec = pickle.loads(message)
            if pickle_dec[0] == 'SEND_DETECTED':
                x = pickle_dec[2][0]
                y = pickle_dec[2][1]
                print(f'Falling people detected! Got the coordinates: {x}, {y}')
            if pickle_dec[0] == 'SEND_UNDETECTED':
                print('Falling people undetected!')

    def send_message(self, data_list):
        payload = pickle.dumps(data_list)
        self.client.send(payload)


if __name__ == '__main__':
    client = Client(SERVER_HOST, SERVER_PORT, NAME)
