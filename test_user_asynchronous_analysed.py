import streamlit as st
import tempfile
import mediapipe as mp
import numpy as np
from PIL import Image, ImageDraw
import cv2

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
        
        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to Pillow Image
        pil_image = Image.fromarray(frame_rgb)

        # Perform pose detection
        result = pose.process(np.array(pil_image))

        # If pose landmarks are detected, draw them on the frame
        if result.pose_landmarks:
            draw = ImageDraw.Draw(pil_image)
            for landmark in result.pose_landmarks.landmark:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 0, 0))
        
        # Append the processed PIL image back to frames
        processed_frames.append(np.array(pil_image))
    
    cap.release()

    # Create a temporary file to save the processed video
    out_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    out_video_path = out_file.name

    # Write the processed frames into a new video file using OpenCV
    out = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for processed_frame in processed_frames:
        out.write(cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR))
    out.release()

    # Display the processed video in the Streamlit app
    st.video(out_video_path)
