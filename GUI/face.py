import cv2
import numpy as np
import tensorflow as tf

# Load pre-trained MobileNetV2 model for liveness detection
model_path = 'path/to/mobilenetv2/model'
liveness_model = tf.keras.models.load_model(model_path)

# Load LBPH face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('path/to/lbph/trained/model.xml')

# Load face cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def preprocess_frame(frame):
    # Preprocess frame for MobileNetV2
    frame = cv2.resize(frame, (224, 224))
    frame = tf.keras.applications.mobilenet_v2.preprocess_input(frame)
    frame = np.expand_dims(frame, axis=0)
    return frame

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    return faces

def recognize_face(face):
    face_roi = gray[y:y+h, x:x+w]
    label, confidence = face_recognizer.predict(face_roi)
    return label, confidence

def liveness_detection(frame):
    preprocessed_frame = preprocess_frame(frame)
    prediction = liveness_model.predict(preprocessed_frame)
    return prediction

# Capture video from the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect faces
    faces = detect_faces(frame)

    for (x, y, w, h) in faces:
        # Recognize the face
        label, confidence = recognize_face(frame[y:y+h, x:x+w])

        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the recognized name and confidence
        cv2.putText(frame, f'Person {label} ({confidence:.2f}%)', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Perform liveness detection
        liveness_result = liveness_detection(frame[y:y+h, x:x+w])

        if liveness_result < 0.5:  # You may need to adjust the threshold
            cv2.putText(frame, 'Liveness: Real', (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Liveness: Fake', (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Attendance System', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
