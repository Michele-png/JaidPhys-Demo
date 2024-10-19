import streamlit as st
import cv2
import mediapipe as mp
import tempfile
import os
from moviepy.editor import VideoFileClip

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def process_video(input_video_path, output_video_path):
    # Read the video
    cap = cv2.VideoCapture(input_video_path)
    frames = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Draw pose landmarks if detected
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Convert back to RGB for Streamlit and MoviePy (from BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame)

    cap.release()

    # Use MoviePy to write video with proper encoding for web
    clip = VideoFileClip(input_video_path)
    new_clip = clip.set_fps(fps).fl_image(lambda img: frames.pop(0))
    new_clip.write_videofile(output_video_path, codec="libx264", audio=False)

# Streamlit Web App Interface
st.title("Pose Estimation on Video")

# File uploader
uploaded_file = st.file_uploader("Upload a video of a person", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    # Show the uploaded video before processing
    st.video(uploaded_file)

    # Process the video and overlay pose estimation lines
    output_path = os.path.join(tempfile.gettempdir(), 'processed_video.mp4')
    st.text("Processing video... this might take a while.")
    process_video(tfile.name, output_path)

    # Convert the processed video to bytes for display
    with open(output_path, 'rb') as video_file:
        video_bytes = video_file.read()

    # Display the processed video using video bytes
    st.text("Here is the processed video:")
    st.video(video_bytes)

    # Allow download of the processed video
    with open(output_path, "rb") as f:
        st.download_button("Download processed video", f, file_name="processed_video.mp4")
