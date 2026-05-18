import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. IMPOSTAZIONE GRAFICA E LOGO
st.set_page_config(page_title="INTEC - Calcolatore ROI", layout="wide")

# Logo INTEC ufficiale
try:
    st.image("INTEC-logo-V1-2colori-POSITIVE.png", width=450)
except:
    st.title("🟢 INTEC SYSTEMS")

st.markdown("### Calcolatore di Efficienza e ROI — *Supporto alla Vendita*")
st.markdown("---")

# 2. CARICAMENTO DATABASE EXCEL
@st.cache_data
def load_data():
    file_path = "Calcolatore Costi INTEC (1).xlsx"
    df_db = pd.read_excel(file_path, sheet_name='Database')
    return df_db

try:
    df_db = load_data()
except Exception as e:
    st.error(f"Errore nel caricamento del database Excel: {e}")
    st.stop()

# 3. SEZIONE INPUT GENERALI
st.markdown("#### 1. Configurazione Cantiere / Progetto")
col_gen1, col_gen2, col_gen3 = st.columns(3)

with col_gen1:
    superficie = st.number_input("Superficie da trattare:", min_value=0.0, value=10.0, step=1.0)
with col_gen2:
    unita = st.selectbox("Unità di Misura:", ["Metri Quadri (m²)", "Piedi Quadri (sq ft)"])
with col_gen3:
    valuta = st.selectbox("Valuta:", ["Euro (€)", "Dollaro ($)"])

st.markdown("---")

# 4. COLONNE PARALLELE DI CONFRONTO
st.markdown("#### 2. Analisi Comparativa Metodi")
col_intec, col_cliente = st.columns(2)

# --- COLONNA SINISTRA: METODO INTEC (AUTOMATICO) ---
with col_intec:
    st.subheader("🟢 Sistema INTEC")
    st.info("I calcoli seguenti sono estratti automaticamente dalle rese di listino.")
    
    kg_pf07e = superficie * 14.0
    kg_r999 = superficie * 0.468
    kg_tot_intec = kg_pf07e + kg_r999
    
    prezzo_intec_base = 10.70
    prezzo_intec_input = st.number_input("Prezzo Materiale INTEC (€/KG o $/KG):", min_value=0.0, value=prezzo_intec_base, step=0.1)
    
    ore_intec = (superficie / 5.0) + 2.0
    st.text(f"Ore Manodopera Stimate (Bloccato): {ore_intec} ore")
    
    costo_orario_intec = st.number_input("Costo Orario Manodopera INTEC:", min_value=0.0, value=25.0, step=1.0)
    
    tot_mat_intec = kg_tot_intec * prezzo_intec_input
    tot_mano_intec = ore_intec * costo_orario_intec
    tot_generale_intec = tot_mat_intec + tot_mano_intec

# --- COLONNA DESTRA: METODO CLIENTE (MANUALE) ---
with col_cliente:
    st.subheader("⚪ Metodo Attuale Cliente")
    tecnologia = st.selectbox("Tecnologia Concorrente:", ["Epossidica", "Spray"])
    
    kg_cliente = st.number_input(f"Quantità
