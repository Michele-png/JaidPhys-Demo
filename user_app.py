import cv2
import av
import numpy as np
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer, WebRtcMode
import mediapipe as mp

class PostureTransformer(VideoTransformerBase):
    def __init__(self, show_pose: bool):
        self.show_pose = show_pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        if self.show_pose:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.pose.process(img_rgb)

            if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    img,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                )
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    st.title("Real-Time Posture Overlay WebApp")
    st.write(
        """
        This web application uses your front camera to display real-time video with postural lines superimposed.
        """
    )

    # User controls
    show_pose = st.sidebar.checkbox("Show Pose Landmarks", value=True)

    # Configure WebRTC
    webrtc_ctx = webrtc_streamer(
        key="posture-overlay",
        mode=WebRtcMode.SENDRECV,
        media_stream_constraints={
            "video": True,
            "audio": False,
        },
        video_processor_factory=lambda: PostureTransformer(show_pose),
        async_processing=True
    )

    if webrtc_ctx.video_transformer and show_pose:
        st.write("Postural lines are being applied to your video stream.")
    
    # Visualizzazione dei feedback
    st.header("Analisi Posturale")

    # Funzione asincrona per leggere feedback dal database
    async def get_feedback():
        try:
            # Inizializza l'app Firebase
            cred = credentials.Certificate(r"C:\Users\User\Downloads\jaidphysdemo-firebase-adminsdk-pxz38-e46d20f07e.json")
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

if __name__ == "__main__":
    main()
