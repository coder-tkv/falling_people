from ultralytics import YOLO

model = YOLO(r'runs\detect\yolov8n_custom3\weights\best.pt')

if __name__ == '__main__':
    # Validate.
    results = model.val(data=r'C:\Users\Егор\PycharmProjects\pythonProject\datasets\fall_people\data.yaml')