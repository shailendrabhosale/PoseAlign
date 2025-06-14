import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import joblib
from itertools import combinations
import subprocess
from mediapipe.framework.formats import landmark_pb2

# Initialize MediaPipe drawing utilities
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Load model and preprocessing tools
model = load_model("enhanced_model.h5")
scaler = joblib.load("enhanced_scaler.pkl")
label_encoder = joblib.load("enhanced_label_encoder.pkl")

MIN_VISIBILITY = 0.6

def get_normalization_factor(landmarks):
    try:
        left_shoulder = landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value]
        left_hip = landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value]
        return np.sqrt((left_shoulder.x - left_hip.x) ** 2 + (left_shoulder.y - left_hip.y) ** 2)
    except:
        return 1.0

def calculate_3d_angle(a, b, c):
    ba = np.array([a.x - b.x, a.y - b.y, a.z - b.z])
    bc = np.array([c.x - b.x, c.y - b.y, c.z - b.z])
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8)
    return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

def get_enhanced_landmarks(results):
    landmarks = []

    if results.pose_landmarks:
        landmarks.extend(results.pose_landmarks.landmark)

        # Add mid-chest point
        left_shoulder = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value]
        mid_chest = landmark_pb2.NormalizedLandmark()
        mid_chest.x = (left_shoulder.x + right_shoulder.x) / 2
        mid_chest.y = (left_shoulder.y + right_shoulder.y) / 2
        mid_chest.z = (left_shoulder.z + right_shoulder.z) / 2
        mid_chest.visibility = (left_shoulder.visibility + right_shoulder.visibility) / 2
        landmarks.append(mid_chest)

    if results.left_hand_landmarks:
        landmarks.extend(results.left_hand_landmarks.landmark)
    if results.right_hand_landmarks:
        landmarks.extend(results.right_hand_landmarks.landmark)

    return landmarks

def extract_features(results):
    features = {}
    landmarks = get_enhanced_landmarks(results)
    norm_factor = get_normalization_factor(landmarks)

    for idx, lm in enumerate(landmarks):
        features[f'lm_{idx}_x'] = lm.x
        features[f'lm_{idx}_y'] = lm.y
        features[f'lm_{idx}_z'] = lm.z
        features[f'lm_{idx}_vis'] = lm.visibility

    for i, j, k in combinations(range(len(landmarks)), 3):
        try:
            angle = calculate_3d_angle(landmarks[i], landmarks[j], landmarks[k])
            features[f'angle_{i}_{j}_{k}'] = angle
        except:
            features[f'angle_{i}_{j}_{k}'] = 0

    for i, j in combinations(range(len(landmarks)), 2):
        dx = (landmarks[i].x - landmarks[j].x) / norm_factor
        dy = (landmarks[i].y - landmarks[j].y) / norm_factor
        dz = (landmarks[i].z - landmarks[j].z) / norm_factor
        features[f'dist_{i}_{j}'] = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    return pd.DataFrame([features]).fillna(0).values

cap = cv2.VideoCapture(0)
cv2.namedWindow('Enhanced Body Analysis', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Enhanced Body Analysis', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

run_back = False

with mp_holistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7, model_complexity=1) as holistic:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        viz_frame = frame.copy()

        mp_drawing.draw_landmarks(
            viz_frame,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
        )
        mp_drawing.draw_landmarks(
            viz_frame,
            results.left_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
        )
        mp_drawing.draw_landmarks(
            viz_frame,
            results.right_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
        )

        features = extract_features(results)
        if features.size > 0:
            try:
                features_scaled = scaler.transform(features)
                pred = model.predict(features_scaled, verbose=0)[0]
                pose_label = label_encoder.inverse_transform([np.argmax(pred)])[0]
                confidence = np.max(pred)
                cv2.putText(viz_frame, f"{pose_label} ({confidence*100:.1f}%)", (20, 60),
                            cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 0, 0), 2)
            except Exception as e:
                print(f"Prediction error: {e}")

        # Add instructions
        cv2.putText(viz_frame, 'Press b to go Back | q to Quit',
                    (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 100, 255), 2)

        viz_frame = cv2.resize(viz_frame, (1920, 1080))
        cv2.imshow('Enhanced Body Analysis', viz_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('b'):
            run_back = (key == ord('b'))
            break

cap.release()
cv2.destroyAllWindows()

if run_back:
    subprocess.Popen(["python", "GUI_main.py"])
