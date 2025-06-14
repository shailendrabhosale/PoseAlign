# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 23:14:35 2025

@author: Atharv
"""

import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import pickle
import time
import os
from gtts import gTTS
import playsound

# ========== Check for Dependencies ==========
try:
    import mediapipe as mp
except ImportError:
    print("Error: mediapipe not found. Run: pip install mediapipe")
    exit()

try:
    import cv2
except ImportError:
    print("Error: OpenCV not found. Run: pip install opencv-python")
    exit()

try:
    import gtts
    import playsound
except ImportError:
    print("Error: gTTS or playsound not found. Run: pip install gTTS playsound")
    exit()

# ========== Load ML Model ==========
with open('body_language.pkl', 'rb') as f:
    model = pickle.load(f)

# ========== MediaPipe Setup ==========
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# ========== Pose Timer Variables ==========
start_time = None
holding_pose = False
pose_hold_time = 0
current_pose = None

# ========== OpenCV Feed ==========
cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = holistic.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            pose = results.pose_landmarks.landmark
            face = results.face_landmarks.landmark
            row = list(np.array([[l.x, l.y, l.z, l.visibility] for l in pose]).flatten()) + \
                  list(np.array([[l.x, l.y, l.z, l.visibility] for l in face]).flatten())

            X = pd.DataFrame([row])
            body_language_class = model.predict(X)[0]
            prob = model.predict_proba(X)[0]
            confidence = round(prob[np.argmax(prob)], 2)

            coords = tuple(np.multiply(
                np.array((results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x,
                          results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y)),
                [640, 480]).astype(int))

            # Draw info on screen
            cv2.rectangle(image, (0, 0), (250, 80), (245, 117, 16), -1)
            cv2.putText(image, 'Pose: ' + body_language_class, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(image, 'Confidence: ' + str(confidence), (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # === Pose Timer Logic ===
            if confidence >= 0.75:
                if not holding_pose or current_pose != body_language_class:
                    start_time = time.time()
                    holding_pose = True
                    current_pose = body_language_class
                else:
                    pose_hold_time = time.time() - start_time
                    cv2.putText(image, f"Held: {int(pose_hold_time)}s", (10, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                if holding_pose:
                    print(f"{current_pose} held for {int(pose_hold_time)} seconds.")
                    if pose_hold_time < 5:
                        msg = "Try to hold the pose longer"
                        tts = gTTS(msg)
                        tts.save("feedback.mp3")
                        playsound.playsound("feedback.mp3")
                        os.remove("feedback.mp3")
                    holding_pose = False
                    pose_hold_time = 0

        except Exception as e:
            print("Detection Error:", e)

        # Render
        cv2.imshow('Yoga Pose with Timer', cv2.resize(image, (1200, 700)))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
