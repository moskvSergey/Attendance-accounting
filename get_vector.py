import dlib
import cv2
import time
from ultralytics import YOLO
import json
import numpy as np


def detect_head(frame):
    results = model.track(frame, iou=0.4, conf=0.5, persist=True, imgsz=608, verbose=False)

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        class_ids = results[0].boxes.cls.cpu().numpy().astype(int)

        for box, id, cls in zip(boxes, ids, class_ids):
            cropped_frame = frame[box[1]:box[3], box[0]:box[2]]
            get_face_vector(cropped_frame)


def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            detect_head(frame)
            time.sleep(1)

def get_face_vector(frame):
    detector = dlib.get_frontal_face_detector()
    shape_predictor_path = 'data/shape_predictor_68_face_landmarks.dat'
    face_rec_model_path = 'data/dlib_face_recognition_resnet_model_v1.dat'

    try:
        shape_predictor = dlib.shape_predictor(shape_predictor_path)
    except RuntimeError as e:
        print(f"Не удалось загрузить shape_predictor: {e}")
        exit(1)

    try:
        face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)
    except RuntimeError as e:
        print(f"Не удалось загрузить face_rec_model: {e}")
        exit(1)
    try:
        img = cv2.imdecode(np.fromstring(frame.read(), np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            shape = shape_predictor(gray, face)
            face_descriptor = face_rec_model.compute_face_descriptor(frame, shape)
            print(face_descriptor)
            face_vector_json = json.dumps(list(face_descriptor))
            return face_vector_json
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    model = YOLO('data/model.pt')
    model.fuse()
    detector = dlib.get_frontal_face_detector()
    shape_predictor_path = 'data/shape_predictor_68_face_landmarks.dat'
    face_rec_model_path = 'data/dlib_face_recognition_resnet_model_v1.dat'

    try:
        shape_predictor = dlib.shape_predictor(shape_predictor_path)
    except RuntimeError as e:
        print(f"Не удалось загрузить shape_predictor: {e}")
        exit(1)

    try:
        face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)
    except RuntimeError as e:
        print(f"Не удалось загрузить face_rec_model: {e}")
        exit(1)

    generate_frames()
