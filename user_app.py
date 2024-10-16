# user_app.py
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import asyncio

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
    key="example",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
)

# Visualizzazione dei feedback
st.header("Feedback dal Socio")

# Funzione asincrona per leggere feedback dal server
async def get_feedback():
    try:
        with open("feedback.txt", "r", encoding="utf-8") as f:
            feedback = f.read()
        return feedback
    except FileNotFoundError:
        return "Nessun feedback disponibile."

# Bottone per aggiornare il feedback
if st.button("Aggiorna Feedback"):
    feedback = asyncio.run(get_feedback())
    st.text_area("Feedback", value=feedback, height=300)
