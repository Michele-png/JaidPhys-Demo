import streamlit as st
import cv2
import mediapipe as mp
import tempfile
import os
import moviepy.editor as mpy

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def process_video(video_path, output_path):
    # Read the video
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Output video writer
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)
        
        if results.pose_landmarks:
            # Draw the pose annotations on the frame
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Write the processed frame to the output video
        out.write(frame)
    
    # Release resources
    cap.release()
    out.release()

# Streamlit Web App Interface
st.title("Pose Estimation on Video")

# File uploader
uploaded_file = st.file_uploader("Upload a video of a person", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    st.video(uploaded_file)  # Show the uploaded video

    # Process the video and overlay pose estimation lines
    output_path = os.path.join(tempfile.gettempdir(), 'processed_video.mp4')
    st.text("Processing video... this might take a while.")
    process_video(tfile.name, output_path)

    # Show the processed video
    st.text("Here is the processed video:")
    st.video(output_path)

    # Allow download of the processed video
    with open(output_path, "rb") as f:
        st.download_button("Download processed video", f, file_name="processed_video.mp4")

