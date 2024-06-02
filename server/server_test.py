import socket
from threading import Thread
import pickle

SERVER_HOST = '192.168.235.164'
SERVER_PORT = 4578
NAME = 'client_pc'
CONFIDENCE_THRESHOLD = 0.6
BLUE = (255, 0, 0)


class Client:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name
        self.client = socket.socket()
        print(f'[*] Connecting to {self.ip}:{self.port} with name {self.name}')
        self.client.connect((self.ip, self.port))
        payload = pickle.dumps(['SEND_NAME', f"{self.name}"])
        self.client.send(payload)
        print(f'[+] Connected with name {self.name}.')
        neural_net_thread = Thread(target=self.send_message)
        neural_net_thread.start()
        neural_net_thread.join()

    def send_message(self):
        input()
        data_list = [f'SEND_DETECTED', 'Falling people detected!', (10, 10)]
        payload = pickle.dumps(data_list)
        self.client.send(payload)


if __name__ == '__main__':
    client = Client(SERVER_HOST, SERVER_PORT, NAME)

