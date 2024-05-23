import time
from ultralytics import YOLO
import cv2
import socket
from threading import Thread

NAME = 'client_pc'
HOSTNAME = 'localhost'
PORT = 4578
data = NAME
CONFIDENCE_THRESHOLD = 0.6
BLUE = (255, 0, 0)

client = socket.socket()
print(f'[*] Connecting to {HOSTNAME}:{PORT} with name {NAME}')
client.connect((HOSTNAME, PORT))
print(f'[+] Connected with name {NAME}.')


def listen_for_messages():
    while True:
        message = client.recv(1024).decode()
        print(message)


def neural_net():
    falling_people_counter = 0
    not_falling_people_counter = 0
    max_errors = 3
    timer = None
    is_falling = False

    video_cap = cv2.VideoCapture(0)
    model = YOLO(r'runs/detect/yolov8n_custom3/weights/best.pt')

    while True:
        ret, frame = video_cap.read()
        width = 1280
        height = 720
        dim = (width, height)

        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        detections = model(frame, verbose=False)[0]
        if detections:
            falling_people_counter += 1
            if not timer:
                timer = time.time()
        else:
            not_falling_people_counter += 1

        if not_falling_people_counter >= max_errors:
            not_falling_people_counter = 0
            falling_people_counter = 0
            timer = None
            if is_falling:
                client.sendall(b'Falling people undetected!')
            is_falling = False
        for data in detections.boxes.data.tolist():
            confidence = data[4]

            if float(confidence) < CONFIDENCE_THRESHOLD:
                continue

            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), BLUE, 2)
            center_x = (xmax + xmin) // 2
            center_y = (ymax + ymin) // 2
            if timer:
                if time.time() > timer + 5.0:
                    if not is_falling:
                        client.sendall(
                            f'Falling people detected. Coordinates: ({center_x}, {center_y})'.encode('utf-8'))
                    is_falling = True
            result = detections[0]
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                cv2.putText(frame, class_id + ' ' + str(round(confidence, 2)) + '%', (xmin, ymin + 23),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    video_cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    listen_for_messages_thread = Thread(target=listen_for_messages)
    listen_for_messages_thread.daemon = True
    neural_net_thread = Thread(target=neural_net)
    neural_net_thread.daemon = True
    neural_net_thread.start()
    listen_for_messages_thread.start()

    while data != 'stop':
        client.sendall(data.encode('utf-8'))
        data = input()
    print('[-] Disconnected.')
    client.close()
