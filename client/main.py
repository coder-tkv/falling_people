import socket

NAME = 'client_pc'
HOSTNAME = 'localhost'
PORT = 4578

client = socket.socket()

print(f'[*] Connecting to {HOSTNAME}:{PORT}')
client.connect((HOSTNAME, PORT))
print('[+] Connected.')
data = NAME
while data != 'stop':
    client.sendall(data.encode('utf-8'))
    print(f'[!] {NAME}: {data}')
    data = input()
print('[-] Disconnected.')
client.close()
