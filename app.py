import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import datetime

# 1. IMPOSTAZIONE GRAFICA E LOGO
st.set_page_config(page_title="INTEC - Proposta ROI", layout="wide")

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return None

logo_positive = get_image_base64("INTEC-logo-V1-2colori-POSITIVE.png")
logo_negative = get_image_base64("INTEC-logo-V1-2colori-NEGATIVE.png")

# CSS AGGIORNATO: MENU VISIBILE SU SCHERMO E STAMPA COMPATTA
st.markdown(f"""
    <style>
        /* 1. Riduce lo spazio in alto ma SALVA il menu a tendina laterale */
        .block-container {{
            padding-top: 2.5rem !important;
            padding-bottom: 0.5rem !important;
        }}
        
        /* 2. Centratura Logo e Spazi */
        .logo-outer-container {{ display: flex; justify-content: center; width: 100%; margin-bottom: -10px; }}
        .logo-container {{ width: 380px; max-width: 100%; }}
        .logo-light {{ display: block; width: 100%; }}
        .logo-dark {{ display: none; width: 100%; }}
        
        @media (prefers-color-scheme: dark) {{
            .logo-light {{ display: none; }}
            .logo-dark {{ display: block; }}
        }}
        
        /* 3. BLINDATURA PER LA STAMPA SU SINGOLA PAGINA (A4) */
        @media print {{
            @page {{ margin: 0.4cm; size: A4 portrait; }} 
            
            /* QUI nascondiamo i menu e i controlli, SOLO durante la stampa! */
            .stButton, .stNumberInput, .stSelectbox, .stDateInput, .stTextInput, header[data-testid="stHeader"], [data-testid="stSidebar"] {{
                display: none !important;
            }}
            
            /* Forza lo sfondo bianco assoluto e testo nero */
            .main, .block-container {{ 
                background-color: white !important; 
                color: black !important; 
                padding: 0 !important; 
                margin: 0 !important;
            }}
            
            /* Logo di stampa ottimizzato */
            .logo-dark {{ display: none !important; }}
            .logo-light {{ display: block !important; width: 200px !important; margin: 0 auto 5px auto !important; }}
            
            /* Forza le colonne a restare affiancate per risparmiare spazio verticale */
            div[data-testid="column"] {{
                width: 48% !important;
                flex: 1 1 48% !important;
                min-width: 48% !important;
                display: inline-block !important;
                vertical-align: top;
            }}
            
            /* Compatta al massimo i blocchi dei Totali */
            div[data-testid="stMetric"] {{
                padding: 2px !important;
                margin: 0 !important;
            }}
            
            /* Compressione dei testi e dei titoli */
            h3, h4, p, ul, li {{ margin-top: 2px !important; margin-bottom: 2px !important; padding: 0 !important; font-size: 13px !important; }}
            hr {{ margin: 4px 0 !important; }}
            
            /* Colore testo grafici nero per la stampa */
            .js-plotly-plot .plotly text {{ fill: #000000 !important; }}
        }}
    </style>
    <div class="logo-outer-container">
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_positive}" class="logo-light">
            <img src="data:image/png;base64,{logo_negative}" class="logo-dark">
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. INTESTAZIONE PERSONALIZZATA
st.markdown("<h3 style='text-align: center; margin-top: 0;'>Calcolatore di Efficienza e ROI — Supporto alla Vendita</h3>", unsafe_allow_html=True)

col_hdr1, col_hdr2 = st.columns(2)
with col_hdr1:
    nome_cliente = st.text_input("👤 Nome Cliente / Cantiere:", placeholder="Es. Cantiere Navale Rossi")
with col_hdr2:
    data_offerta = st.date_input("📅 Data Offerta:", value=datetime.date.today(), format="DD/MM/YYYY")

st.markdown("---")

# 3. CARICAMENTO DATABASE
@st.cache_data
def load_data():
    file_path = "Calcolatore Costi INTEC (1).xlsx"
    return pd.read_excel(file_path, sheet_name='Database')

try:
    df_db = load_data()
except Exception as e:
    st.error(f"Errore caricamento database: {e}")
    st.stop()

# 4. CONFIGURAZIONE CANTIERE
st
