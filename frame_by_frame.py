import streamlit as st
import cv2 as cv
import tempfile
import mediapipe as mp
import time
import os
import json
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore

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
    delay = 5 / fps if fps > 0 else 0.03  # Adjust delay based on video fps
    st.write(f"delay: {delay}")
    n_skipped = 5
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
        if frame_counter % n_skipped == 0:  # Only update every n frames
            # Add a delay to control frame rendering speed
            time.sleep(delay)
            stframe.image(frame, channels="BGR", use_column_width=True)  # Display in original color (BGR format)
            # Display current frame number
            st.write(f"Current frame: {frame_counter}")

        

        

        frame_counter += 1  # Increment frame counter

    vf.release()  # Release video capture object

# Funzione asincrona per leggere feedback dal database
async def get_feedback():
    try:
        # Inizializza l'app Firebase
        cred = credentials.Certificate(**st.secrets.FIREBASE_SERVICE_ACCOUNT_KEY)
        try:
            user_app = firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f'{e}')

        db = firestore.client()

        feedback_ref = db.collection('feedback').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
        feedback = feedback_ref.stream()
        if feedback: 
            for fb in feedback:
                return (fb.to_dict()['content'])
        else:
            return "Nessun feedback disponibile."
    except Exception as e:
        return f"Errore nella lettura del feedback: {e}"

# Bottone per aggiornare il feedback
if st.button("Aggiorna Feedback"):
    feedback = asyncio.run(get_feedback())
    st.text_area("Feedback", value=feedback, height=300, disabled=True)
    try:
        firebase_admin.delete_app(user_app)
        st.success("Connessione a Firebase chiusa con successo!")
    except Exception as e:
        st.error(f"Errore nella chiusura della connessione a Firebase: {e}")
