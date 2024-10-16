# user_app.py
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import asyncio
import sqlite3

st.set_page_config(
    page_title="Interfaccia Spettatore - Video Personale",
    layout="centered",
)

st.title("Interfaccia Spettatore - Video Personale")

# Classe per trasformare il video, se necessario
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # Puoi aggiungere trasformazioni all'immagine qui, se necessario
        return img

# Avvia lo streamer
webrtc_ctx = webrtc_streamer(
    key="spettatore-video",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
)

# Visualizzazione dei feedback
st.header("Feedback dal Socio")

# Funzione asincrona per leggere feedback dal database
async def get_feedback():
    try:
        conn = sqlite3.connect('feedback.db')
        c = conn.cursor()
        c.execute("SELECT content FROM feedback ORDER BY id DESC LIMIT 1")
        feedback = c.fetchone()
        conn.close()
        if feedback:
            return feedback[0]
        else:
            return "Nessun feedback disponibile."
    except Exception as e:
        return f"Errore nella lettura del feedback: {e}"

# Bottone per aggiornare il feedback
if st.button("Aggiorna Feedback"):
    feedback = asyncio.run(get_feedback())
    st.text_area("Feedback", value=feedback, height=300, disabled=True)
