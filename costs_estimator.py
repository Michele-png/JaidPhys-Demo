import streamlit as st

def main():
    st.title("Calcolatore di Impatto DSE e Problemi Muscoloscheletrici")
    st.write(
        """
        Inserisci il numero di dipendenti della tua azienda per calcolare i seguenti valori:
        - Giorni spesi per la gestione della conformità DSE.
        - Giorni spesi dai dipendenti per completare valutazioni tradizionali DSE.
        - Giorni persi a causa di assenze per problemi muscoloscheletrici.
        - Giorni persi per riduzione di produttività correlata ai problemi muscoloscheletrici.
        """
    )
    
    # Input: Numero di dipendenti
    num_employees = st.number_input("Inserisci il numero di dipendenti", min_value=1, step=1, value=10)
    
    # Calcoli
    # Giorni spesi per la gestione della conformità DSE
    days_admin_dse = (num_employees * 10) / 60 / 8  # 10 minuti per dipendente, convertito in giorni
    
    # Giorni spesi per completare valutazioni tradizionali DSE
    days_training_dse = (num_employees * 45) / 60 / 8  # 45 minuti per dipendente, convertito in giorni
    
    # Giorni persi per assenze per problemi muscoloscheletrici
    msk_absence_rate = 0.026  # 2.6% del personale
    msk_absence_days = num_employees * msk_absence_rate * 20  # 4 settimane di assenza = 20 giorni lavorativi
    
    # Giorni persi per riduzione di produttività correlata ai problemi muscoloscheletrici
    msk_pain_incidence = 0.15  # 15% del personale
    msk_productivity_loss = 0.15  # 15% di perdita di produttività
    msk_loss_days = num_employees * msk_pain_incidence * msk_productivity_loss * 220  # 220 giorni lavorativi annui
    
    # Output
    st.subheader("Risultati")
    st.write("I valori sono stimati considerando un giorno lavorativo di 8 ore.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Giorni spesi per la gestione della conformità DSE",
            value=f"{days_admin_dse:.2f}"
        )
        st.metric(
            label="Giorni persi per riduzione di produttività correlata ai problemi muscoloscheletrici",
            value=f"{msk_loss_days:.2f}"
        )
    
    with col2:
        st.metric(
            label="Giorni spesi dai dipendenti per completare valutazioni tradizionali DSE",
            value=f"{days_training_dse:.2f}"
        )
        st.metric(
            label="Giorni persi per assenze dovute a problemi muscoloscheletrici",
            value=f"{msk_absence_days:.2f}"
        )

if __name__ == "__main__":
    main()
