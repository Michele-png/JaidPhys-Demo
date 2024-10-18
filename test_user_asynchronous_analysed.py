import streamlit as st
import cv2
import tempfile
import mediapipe as mp
import numpy as np

# Initialize Mediapipe pose detector
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Set the title of the app
st.title("Video Posture Recognition App")

# Add a file uploader for video input
video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])

# Check if a video file has been uploaded
if video_file is not None:
    # Save the uploaded video to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(video_file.read())

    # Read the video using OpenCV
    cap = cv2.VideoCapture(tfile.name)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Prepare a list to store processed frames
    processed_frames = []

    # Process the video frame by frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to RGB (Mediapipe uses RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Perform pose detection
        result = pose.process(frame_rgb)
        
        # If pose landmarks are detected, draw them on the frame
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, 
                result.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
            )
        
        # Convert back to BGR (for OpenCV compatibility) and save the processed frame
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        processed_frames.append(frame_bgr)
    
    cap.release()
    
    # Create a temporary file to save the processed video
    out_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    out_video_path = out_file.name

    # Write the processed frames into a new video file
    out = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for processed_frame in processed_frames:
        out.write(processed_frame)
    out.release()

    # Display the processed video in the Streamlit app
    st.video(out_video_path)
