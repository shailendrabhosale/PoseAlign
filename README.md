# YogaAlign: Yoga Posture Detection using Machine Learning

**Short & Catchy:** Your AI Yoga Coach: Instant Posture Feedback for Safer, Smarter Practice

> Final Year Project - B.E. Computer Engineering, Group 12

## 🌟 Project Overview

**YogaAlign** helps people practice yoga safely by giving real-time feedback on their posture using a computer’s camera. It flags incorrect poses and suggests corrections to reduce the risk of injury.

## 🎯 Key Goals

* **User Safety & Experience:** Ensure practitioners maintain healthy alignment.
* **Innovation & Impact:** Demonstrate practical AI/vision skills in a real-world wellness application.
* **Team Collaboration:** Showcase end-to-end project development: research, design, implementation, and testing.

## 🔍 Brief Technological Explanation

* **AI Model for Pose Recognition:** We trained a machine learning model (CNN) that learns common yoga postures from images and can recognize them in video frames. Think of it as teaching a computer to “see” and label body shapes.
* **Body Landmark Detection:** Tools like Mediapipe and PoseNet detect key points on the body (e.g., elbows, knees) so the system understands how limbs are positioned. This is similar to how fitness apps track movement.
* **Image Processing:** OpenCV handles the video feed from a webcam, processes each frame, and overlays guidance feedback (e.g., highlighting misaligned joints).
* **Integration & Real-Time Feedback:** Combining these technologies lets the application analyze posture on the fly, providing immediate visual or textual cues.


## 📂 Project Structure

```
YogaAlign/
├── src/                  # Core code: pose detection, classification, feedback logic
├── model/                # Trained AI model and related files
├── dataset/              # Labeled images used for training
├── GUI_main.py           # Starts the User Interface for camera feed and analysis
├── requirements.txt      # Python dependencies list
└── README.md             # This document
```

## 💻 Setup & Demo

1. **Clone & Install:** Download the repository and install dependencies (listed in `requirements.txt`).
2. **Run Application:** Launch `main.py` to start webcam-based posture analysis.
3. **Observe Feedback:** The system displays detected pose and highlights areas needing adjustment.

## 🤝 Team & Roles

* **Shailendra Sanjeevkumar Bhosale:** Machine model design and training.
* **Chirantan Chaudhari:** System Integration & Developing UI feedback.
* **Atharv Dabhade:** Handled model's body landmark integration and image processing modules.
* **Sairaj Deshmukh:** Managed overall system architecture and documentation.

## 📈 Impact & Future Prospects

* **Practical Skills Demonstration:** Shows proficiency in AI, computer vision, and software integration—valuable for roles in ML engineering, software development, and product design.
* **Scalability Ideas:** Potential to extend into mobile apps, wearable integration, or virtual coaching platforms.

## Thank You!!!
