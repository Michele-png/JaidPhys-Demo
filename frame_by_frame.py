import streamlit as st
import cv2 as cv
import tempfile
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Streamlit Web App Interface
st.title("Pose Estimation on Video")

# File uploader
uploaded_file = st.file_uploader("Upload a video of a person", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    # Open the video file using OpenCV
    vf = cv.VideoCapture(tfile.name)

    stframe = st.empty()  # Placeholder for displaying frames

    # Frame rate control (for smooth playback)
    fps = vf.get(cv.CAP_PROP_FPS)
    delay = 1 / fps if fps > 0 else 0.03  # Adjust delay based on video fps

    while vf.isOpened():
        ret, frame = vf.read()
        # If frame is read correctly ret is True
        if not ret:
            st.text("Can't receive frame (stream end?). Exiting ...")
            break
        
        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Draw pose landmarks on the frame
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Convert the frame back to BGR for display
        # Display the processed frame in Streamlit in color
        stframe.image(frame, channels="BGR")  # Display in original color (BGR format)

        # Add a delay to control frame rendering speed
        time.sleep(delay)

    vf.release()  # Release video capture object