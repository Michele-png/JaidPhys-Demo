import streamlit as st
import cv2
import mediapipe as mp
import tempfile
import os
import subprocess

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def process_video(input_video_path, output_video_path):
    cap = cv2.VideoCapture(input_video_path)
    
    # Get frame properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Using 'mp4v' codec for compatibility
    
    # Create video writer object
    temp_output_path = output_video_path + '.tmp.mp4'  # Temporary output before re-encoding
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width, height))
    
    # Process video frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame from BGR to RGB for pose detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Perform pose detection
        results = pose.process(rgb_frame)
        
        # Draw pose landmarks if detected
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Write the processed frame to the output video (back to BGR for OpenCV)
        out.write(frame)

    # Release resources
    cap.release()
    out.release()

    # Re-encode video to ensure browser compatibility using ffmpeg
    subprocess.run([
        'ffmpeg', '-i', temp_output_path, '-vcodec', 'libx264', '-crf', '28', '-preset', 'slow', output_video_path
    ], check=True)

    # Clean up temporary file
    os.remove(temp_output_path)

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
