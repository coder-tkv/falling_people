import socket
import time
from threading import Thread
import pickle
import OPi.GPIO as GPIO

SERVER_HOST = '192.168.235.164'
SERVER_PORT = 4578
NAME = 'client_robot'
IN1 = 'PH3'
IN2 = 'PH4'
IN3 = 'PH5'
IN4 = 'PH6'


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
                self.forward()
                time.sleep(3)
                self.left()
                time.sleep(0.3)
                self.forward()
                time.sleep(3)
                self.stop()
            if pickle_dec[0] == 'SEND_UNDETECTED':
                print('Falling people undetected!')

    def send_message(self, data_list):
        payload = pickle.dumps(data_list)
        self.client.send(payload)

    def forward(self):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)

    def back(self):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)

    def left(self):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)

    def right(self):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)

    def stop(self):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)


if __name__ == '__main__':
    GPIO.setmode(GPIO.SUNXI)
    GPIO.setwarnings(False)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    client = Client(SERVER_HOST, SERVER_PORT, NAME)
