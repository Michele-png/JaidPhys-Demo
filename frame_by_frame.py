import streamlit as st
import cv2 as cv
import tempfile
import mediapipe as mp
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
    st.write(f"fps: {fps}")
    delay = 1.5 / fps if fps > 0 else 0.03  # Adjust delay based on video fps
    st.write(f"delay: {delay}")
    total_frames = int(vf.get(cv.CAP_PROP_FRAME_COUNT))
    st.write(f"Total frames in video: {total_frames}")

    frame_counter = 0  # Initialize frame counter

    while vf.isOpened():
        ret, frame = vf.read()
        if not ret:
            st.text(f"Can't receive frame at frame number {frame_counter} (stream end?). Exiting ...")
            break

        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Draw pose landmarks on the frame
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Update the display conditionally to avoid overload
        if frame_counter % 1 == 0:  # Only update every n frames
            stframe.image(frame, channels="BGR", use_column_width=True)  # Display in original color (BGR format)

        # Display current frame number
        st.write(f"Current frame: {frame_counter}")

        # Add a delay to control frame rendering speed
        time.sleep(delay)

        frame_counter += 1  # Increment frame counter

    vf.release()  # Release video capture object
