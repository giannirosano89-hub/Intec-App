import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import datetime

# 1. IMPOSTAZIONE GRAFICA E LOGO (Configurazione Nativa Streamlit)
st.set_page_config(
    page_title="Intec App", 
    page_icon="INTEC-logo-V1-2colori-NEGATIVE.png", 
    layout="wide"
)

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
        .block-container {{ padding-top: 2.5rem !important; padding-bottom: 0.5rem !important; }}
        .logo-outer-container {{ display: flex; justify-content: center; width: 100%; margin-bottom: -10px; }}
        .logo-container {{ width: 380px; max-width: 100%; }}
        .logo-light {{ display: block; width: 100%; }}
        .logo-dark {{ display: none; width: 100%; }}
        
        @media (prefers-color-scheme: dark) {{
            .logo-light {{ display: none; }}
            .logo-dark {{ display: block; }}
        }}
        
        @media print {{
            @page {{ margin: 0.4cm; size: A4 portrait; }} 
            .stButton, .stNumberInput, .stSelectbox, .stDateInput, .stTextInput, header[data-testid="stHeader"], [data-testid="stSidebar"] {{
                display: none !important;
            }}
            .main, .block-container {{ background-color: white !important; color: black !important; padding: 0 !important; margin: 0 !important; }}
            .logo-dark {{ display: none !important; }}
            .logo-light {{ display: block !important; width: 200px !important; margin: 0 auto 5px auto !important; }}
            div[data-testid="column"] {{ width: 48% !important; flex: 1 1 48% !important; min-width: 48% !important; display: inline-block !important; vertical-align: top; }}
            div[data-testid="stMetric"] {{ padding: 2px !important; margin: 0 !important; }}
            h3, h4, p, ul, li {{ margin-top: 2px !important; margin-bottom: 2px !important; padding: 0 !important; font-size: 13px !important; }}
            hr {{ margin: 4px 0 !important; }}
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
st.markdown("<h3 style='text-align: center; margin-top: 0;'>Calcolatore di Efficienza e ROI</h3>", unsafe_allow_html=True)

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
st.markdown("#### 1. Configurazione Progetto")
col_gen1, col_gen2, col_gen3 = st.columns(3)

with col_gen1:
    superficie = st.number_input("Superficie da trattare:", min_value=0.0, value=10.0, step=1.0)
with col_gen2:
    unita = st.selectbox("Unità di Misura:", ["Metri Quadri (m²)", "Piedi Quadri (sq ft)"])
with col_gen3:
    valuta = st.selectbox("Valuta:", ["Euro (€)", "Dollaro ($)"])

st.markdown("---")

# 5. ANALISI COMPARATIVA
st.markdown("#### 2. Analisi Comparativa Materiali e Tempi")
col_intec, col_cliente = st.columns(2)

# Variabile per il controllo del Mercato USA
is_us_market = (unita == "Piedi Quadri (sq ft)" and valuta == "Dollaro ($)")

# --- COLONNA INTEC ---
with col_intec:
    st.subheader("🟢 Sistema INTEC")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        prodotto_intec = st.selectbox("Prodotto:", ["PF07E", "PF07LS", "PF10E", "PF10GT", "PV10E"])
    with col_sel2:
        tipo_rinforzo = st.selectbox("Tipo di Rinforzo:", ["MAT 300", "MAT 450", "OZ 1.0", "OZ 1.5"])
    
    # Conversione Superfici
    if unita == "Metri Quadri (m²)":
        superficie_m2 = superficie
        superficie_sqft = superficie * 10.7639
    else:
        superficie_sqft = superficie
        superficie_m2 = superficie / 10.7639
    
    moltiplicatori_r999 = {
        "MAT 300": 1.5,      
        "MAT 450": 2.25,     
        "OZ 1.0": 0.312,     
        "OZ 1.5": 0.468      
    }
    
    # Calcolo resina R999
    if "MAT" in tipo_rinforzo:
        kg_r999 = superficie_m2 * moltiplicatori_r999[tipo_rinforzo]
        display_r999 = kg_r999
        unita_r999 = "kg"
    else: 
        lbs_r999 = superficie_sqft * moltiplicatori_r999[tipo_rinforzo]
        kg_r999 = lbs_r999 / 2.20462  
        display_r999 = lbs_r999
        unita_r999 = "lbs"
        
    # --- MOTORE MATEMATICO CONTENITORI R999 (Soglia 175 kg) ---
    if kg_r999 < 175.0:
        latte_r999 = kg_r999 / 25.0
        if is_us_market:
            testo_r999 = f"{display_r999:.2f} {unita_r999} [{latte_r999:.1f} pails (25 kg)] — *laminazione 2 strati*"
        else:
            testo_r999 = f"{display_r999:.2f} {unita_r999} [{latte_r999:.1f} latte (da 25 kg)] — *laminazione 2 strati*"
    else:
        fusti_r999 = kg_r999 / 225.0
        if is_us_market:
            galloni_r999 = fusti_r999 * 55.0
            testo_r999 = f"{display_r999:.2f} {unita_r999} [{galloni_r999:.1f} gallons / {fusti_r999:.1f} drums from 55 gal] — *laminazione 2 strati*"
        else:
            testo_r999 = f"{display_r999:.2f} {unita_r999} [{fusti_r999:.1f} fusti (da 225 kg)] — *laminazione 2 strati*"

    # --- MOTORE MATEMATICO PRODOTTI BASE (Volume fisso, peso variabile) ---
    peso_specifico = 0.7 if "07" in prodotto_intec else 1.0
    consumo_m2 = 20.0 * peso_specifico
    peso_fusto = 200.0 * peso_specifico
    
    # Calcolo materiale base
    kg_prodotto = superficie_m2 * consumo_m2
    fusti_prodotto = kg_prodotto / peso_fusto 
    
    # Formattazione condizionale senza i 200lt
    if is_us_market:
        galloni_per_fusto = 55.0  
        tot_galloni = fusti_prodotto * galloni_per_fusto
        spessore_inch = 16 / 25.4
        testo_prodotto = f"{tot_galloni:.1f} gallons ({fusti_prodotto:.1f} drums from 55 gal) — *thickness {spessore_inch:.2f} inch*"
    else:
        testo_prodotto = f"{fusti_prodotto:.1f} fusti (da {peso_fusto:.0f} kg) — *spessore 16mm*"

    st.markdown(f"""
    **Specifiche Tecniche:**
    - 📦 **{prodotto_intec}:** {testo_prodotto}
    - 🧪 **Resina R999 ({tipo_rinforzo}):** {testo_r999}
    """)
    
    # Inserimento Prezzi Separati INTEC
    col_prezzi1, col_prezzi2 = st.columns(2)
    with col_prezzi1:
        prezzo_intec_label = f"Prezzo {prodotto_intec} ($/lbs):" if is_us_market else f"Prezzo {prodotto_intec} (€/KG):"
        prezzo_intec_input = st.number_input(prezzo_intec_label, min_value=0.0, value=10.70, step=0.1)
    with col_prezzi2:
        prezzo_resina_label = "Costo Resina R999 ($/lbs):" if is_us_market else "Costo Resina R999 (€/KG):"
        prezzo_resina_input = st.number_input(prezzo_resina_label, min_value=0.0, value=5.00, step=0.1)
    
    ore_intec = (superficie_m2 / 5.0) + 2.0
    st.success(f"⏱️ Ore Manodopera Stimate: {ore_intec:.1f} h")
    
    # Calcolo totale economico separato INTEC
    if is_us_market:
        costo_prodotto = (kg_prodotto * 2.20462) * prezzo_intec_input
        costo_resina = (
