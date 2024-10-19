import streamlit as st
import cv2 as cv
import tempfile
import mediapipe as mp

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

        # Convert the frame to grayscale
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Display the processed frame in Streamlit
        stframe.image(gray_frame, channels="GRAY")

    vf.release()  # Release video capture object
