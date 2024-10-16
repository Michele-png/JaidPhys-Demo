# socio_app.py
import streamlit as st
import os

st.set_page_config(
    page_title="Interfaccia Socio - Inserimento Feedback",
    layout="centered",
)

st.title("Interfaccia Socio - Inserimento Feedback")
st.write("Inserisci il feedback che vuoi inviare allo spettatore.")

# Campo di input per il feedback
feedback_input = st.text_area("Feedback sullo spettatore:", height=300)

# Pulsante per inviare il feedback
if st.button("Invia Feedback"):
    try:
        with open("feedback.txt", "w", encoding="utf-8") as f:
            f.write(feedback_input)
        st.success("Feedback inviato con successo!")
    except Exception as e:
        st.error(f"Errore nell'invio del feedback: {e}")

# Opzione per mostrare il contenuto di feedback.txt (debugging)
if st.checkbox("Mostra contenuto di feedback.txt"):
    if os.path.exists("feedback.txt"):
        try:
            with open("feedback.txt", "r", encoding="utf-8") as f:
                feedback = f.read()
            st.text_area("Contenuto di feedback.txt:", value=feedback, height=200)
        except Exception as e:
            st.error(f"Errore nella lettura del file: {e}")
    else:
        st.write("Il file feedback.txt non esiste.")
