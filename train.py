from ultralytics import YOLO

model = YOLO('yolov8n.pt')

if __name__ == '__main__':
    # Training.
    results = model.train(
        data=r'C:\Users\Егор\PycharmProjects\pythonProject\datasets\fall_people\data.yaml',
        imgsz=640,
        epochs=50,
        batch=8,
        name='yolov8n_custom',
        plots=True
    )
