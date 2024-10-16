import cv2
import streamlit as st
import numpy as np
import mediapipe as mp
import time

def capture_and_display():
    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    mp_drawing = mp.solutions.drawing_utils

    # Initialize video capture (0 for default webcam)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        st.error("Cannot access webcam. Please ensure it is connected and not being used by another application.")
        return

    # Define a placeholder for the video frames
    frame_placeholder = st.empty()

    # Continuously capture frames from the webcam
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to grab frame from webcam.")
            break

        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Convert the frame color to RGB for MediaPipe
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and detect pose landmarks
        results = pose.process(image_rgb)

        # If landmarks are detected, draw them on the frame
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )

        # Convert the processed frame back to RGB for displaying in Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the frame in the Streamlit app
        frame_placeholder.image(frame_rgb, channels="RGB")

        # Control the frame rate (approx. 30 FPS)
        time.sleep(0.03)

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def main():
    st.title("Real-Time Posture Overlay WebApp")
    st.write(
        """
        This application accesses your front camera to display a live video feed with posture lines superimposed.
        """
    )

    # Start capturing and displaying video
    capture_and_display()

if __name__ == "__main__":
    main()
