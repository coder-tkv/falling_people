from ultralytics import YOLO
import cv2

CONFIDENCE_THRESHOLD = 0.6
BLUE = (255, 0, 0)

video_cap = cv2.VideoCapture(0)
model = YOLO(r'runs/detect/yolov8n_custom3/weights/best.pt')

while True:
    ret, frame = video_cap.read()
    width = 1500
    height = 1080
    dim = (width, height)

    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    detections = model(frame)[0]
    for data in detections.boxes.data.tolist():
        confidence = data[4]

        if float(confidence) < CONFIDENCE_THRESHOLD:
            continue

        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), BLUE, 2)
        result = detections[0]
        for box in result.boxes:
            class_id = result.names[box.cls[0].item()]
            cv2.putText(frame, class_id + ' ' + str(round(confidence, 2)) + '%', (xmin, ymin + 23), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

video_cap.release()
cv2.destroyAllWindows()
