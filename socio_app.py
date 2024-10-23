# socio_app.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore


# setup web app page
try: 
    st.set_page_config(
        page_title="Interfaccia Socio - Inserimento Feedback",
        layout="centered",
    )
    st.title("Interfaccia Socio - Inserimento Feedback")
    st.write("Inserisci il feedback che vuoi inviare allo spettatore.")
    feedback_input = st.text_area("Feedback sullo spettatore:", height=300)
    # action = st.selectbox('Azioni', ['Seleziona...', 'Chiudi l\'app Firebase'])
except Exception as e:
    st.error(f"Errore nel setup della pagina: {e}")

# Initialize App Firebase
try:
    # Load the TOML content from an environment variable
    credentials_data = st.secrets.FIREBASE_SERVICE_ACCOUNT_KEY
except Exception as e:
    st.error(f"Errore nella lettura delle credenziali: {e}")
    
try:
    cred = credentials.Certificate({
        "type": credentials_data.type,
        "project_id": credentials_data.project_id,
        "private_key_id": credentials_data.private_key_id,
        "private_key": credentials_data.private_key.replace("\\n", "\n"),  # replace line breaks
        "client_email": credentials_data.client_email,
        "client_id": credentials_data.client_id,
        "auth_uri": credentials_data.auth_uri,
        "token_uri": credentials_data.token_uri,
        "auth_provider_x509_cert_url": credentials_data.auth_provider_x509_cert_url,
        "client_x509_cert_url": credentials_data.client_x509_cert_url,
        "universe_domain": credentials_data.universe_domain
    })
except Exception as e:
    st.error(f"Errore nella conversione delle credenziali: {e}")
    
try:
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
except Exception as e:
    st.error(f"Errore nello stabilire una connessione: {e}")

# Ottieni una istanza di Firestore
try:
    db = firestore.client()
except Exception as e:
    st.error(f"Errore nella creazione di un'istanza Firebase: {e}")

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
