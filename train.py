# yolo task=detect mode=train model=yolov8n.pt name=yolov8n_custom data=C:\Users\Егор\PycharmProjects\pythonProject\datasets\fall_people\data.yaml epochs=25 batch=8 imgsz=640 plots=True
# C:\Users\Егор\PycharmProjects\pythonProject

from ultralytics import YOLO

model = YOLO('yolov8n.pt')

if __name__ == '__main__':
    # Training.
    results = model.train(
        data=r'C:\Users\Егор\PycharmProjects\pythonProject\datasets\fall_people\data.yaml',
        imgsz=640,
        epochs=25,
        batch=8,
        name='yolov8n_custom',
        plots=True
    )
