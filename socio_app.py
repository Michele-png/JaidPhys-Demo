# socio_app.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore


# setup web app page
st.set_page_config(
    page_title="Interfaccia Socio - Inserimento Feedback",
    layout="centered",
)

st.title("Interfaccia Socio - Inserimento Feedback")
st.write("Inserisci il feedback che vuoi inviare allo spettatore.")

# Campo di input per il feedback
feedback_input = st.text_area("Feedback sullo spettatore:", height=300)
action = st.selectbox('Azioni', ['Seleziona...', 'Chiudi l\'app Firebase'])



# Inizializza l'app Firebase
cred = credentials.Certificate(r"C:\Users\User\Downloads\jaidphysdemo-firebase-adminsdk-pxz38-e46d20f07e.json")
try:
    user_app = firebase_admin.initialize_app(cred)
except Exception as e:
    st.error(f'{e}')

# Ottieni una istanza di Firestore
db = firestore.client()


# Pulsante per inviare il feedback
if st.button("Invia Feedback"):
    if feedback_input.strip() == '': 
        st.error('Feedback Cannot be Empty')
    else: 
        try:
            # add new document in feedback collection
            db.collection('feedback').add({
                'content': feedback_input,
                'timestamp': firestore.SERVER_TIMESTAMP,
            })
            st.success("Feedback inviato con successo!")
        except Exception as e:
            st.error(f"Errore nell'invio del feedback: {e}")

# Opzione per mostrare il contenuto dei feedback (debugging)
if st.checkbox("Mostra Feedback"):
    try:
        # show message content
        feedback_ref = db.collection('feedback').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
        feedbacks = feedback_ref.stream()
        for fb in feedbacks:
            st.text_area("Feedback:", value=fb.to_dict()['content'], height=200, disabled=True)      
    except Exception as e:
        st.error(f"Errore nella lettura dei feedback: {e}")

if action == 'Chiudi l\'app Firebase':
    try:
        firebase_admin.delete_app(user_app)
        st.success("Connessione a Firebase chiusa con successo!")
    except Exception as e:
        st.error(f"Errore nella chiusura della connessione a Firebase: {e}")