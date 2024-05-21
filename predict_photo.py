from ultralytics import YOLO

model = YOLO(r'runs\detect\yolov8n_custom2\weights\best.pt')

if __name__ == '__main__':
    # Predict.
    results = model.predict(
        conf=0.25,
        source=r'C:\Users\Егор\PycharmProjects\pythonProject\datasets\fall_people\test\images',
        save=True
    )
    