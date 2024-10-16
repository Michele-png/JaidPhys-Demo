# socio_app.py
import streamlit as st
import sqlite3

# Connessione al database (crea il database se non esiste)
conn = sqlite3.connect('feedback.db')
c = conn.cursor()

# Creazione della tabella se non esiste
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
''')
conn.commit()

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
        c.execute("INSERT INTO feedback (content) VALUES (?)", (feedback_input,))
        conn.commit()
        st.success("Feedback inviato con successo!")
    except Exception as e:
        st.error(f"Errore nell'invio del feedback: {e}")

# Opzione per mostrare il contenuto dei feedback (debugging)
if st.checkbox("Mostra Feedback"):
    try:
        c.execute("SELECT content FROM feedback ORDER BY id DESC")
        feedbacks = c.fetchall()
        for fb in feedbacks:
            st.text_area("Feedback:", value=fb[0], height=200, disabled=True)
    except Exception as e:
        st.error(f"Errore nella lettura dei feedback: {e}")

conn.close()
