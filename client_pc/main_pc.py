import socket
from threading import Thread
import pickle
import cv2
import time
from ultralytics import YOLO

SERVER_HOST = '192.168.98.164'
SERVER_PORT = 4578
NAME = 'client_pc'
CONFIDENCE_THRESHOLD = 0.6
CAPTURE_DEVICE = 0
BLUE = (255, 0, 0)


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
        neural_net_thread = Thread(target=self.neural_net)
        neural_net_thread.start()
        neural_net_thread.join()

    def send_message(self, data_list):
        payload = pickle.dumps(data_list)
        self.client.send(payload)

    def neural_net(self):
        falling_people_counter = 0
        not_falling_people_counter = 0
        max_errors = 3
        timer = None
        is_falling = False

        video_cap = cv2.VideoCapture(CAPTURE_DEVICE)
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
                    payload = ['SEND_UNDETECTED', 'Falling people undetected!']
                    print('Falling people undetected!')
                    self.send_message(payload)
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
                            payload = [f'SEND_DETECTED', 'Falling people detected!', (center_x, center_y)]
                            print('Falling people detected!', (center_x, center_y))
                            self.send_message(payload)
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
    client = Client(SERVER_HOST, SERVER_PORT, NAME)
