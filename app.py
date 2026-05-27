import streamlit as st
import plotly.graph_objects as go
import base64
import datetime

# 1. IMPOSTAZIONE GRAFICA E LOGO
st.set_page_config(page_title="Intec App", page_icon="INTEC-logo-V1-2colori-NEGATIVE.png", layout="wide")

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return None

logo_positive = get_image_base64("INTEC-logo-V1-2colori-POSITIVE.png")
logo_negative = get_image_base64("INTEC-logo-V1-2colori-NEGATIVE.png")

# CSS AGGIORNATO: GESTIONE STAMPA, LOGO E SCHERMATE DINAMICHE
st.markdown(f"""
    <style>
        .block-container {{ padding-top: 2.5rem !important; padding-bottom: 0.5rem !important; }}
        .logo-outer-container {{ display: flex; justify-content: center; width: 100%; margin-bottom: -10px; }}
        .logo-container {{ width: 380px; max-width: 100%; }}
        .logo-light {{ display: block; width: 100%; }}
        .logo-dark {{ display: none; width: 100%; }}
        
        .print-text {{ display: none; }}
        
        @media (prefers-color-scheme: dark) {{
            .logo-light {{ display: none; }}
            .logo-dark {{ display: block; }}
        }}
        
        @media print {{
            @page {{ margin: 0.5cm; size: A4 portrait; }} 
            .stButton, .stNumberInput, .stSelectbox, .stDateInput, .stTextInput, header, footer, #MainMenu {{
                display: none !important;
            }}
            .print-text {{ display: block !important; font-size: 13px !important; color: black !important; margin-bottom: 8px !important; line-height: 1.4 !important; }}
            .main, .block-container {{ background-color: white !important; color: black !important; padding: 0 !important; margin: 0 !important; }}
            .logo-dark {{ display: none !important; }}
            .logo-light {{ display: block !important; width: 250px !important; margin: 0 auto 10px auto !important; }}
            
            /* GRAFICI A DIMENSIONE FISSA IN STAMPA */
            .stPlotlyChart {{ width: 330px !important; margin: 0 auto !important; display: block !important; }}
            
            div[data-testid="column"] {{ width: 48% !important; flex: 1 1 48% !important; display: inline-block !important; vertical-align: top; }}
            div[data-testid="stMetric"] {{ padding: 0 !important; margin: 0 !important; }}
            div[data-testid="stAlert"] {{ background-color: white !important; border: 2px solid #008F99 !important; padding: 10px !important; color: black !important; margin-bottom: 5px !important; }}
            div[data-testid="stAlert"] * {{ color: black !important; }}
            h3 {{ font-size: 16px !important; margin-top: 5px !important; margin-bottom: 5px !important; }}
            h4 {{ font-size: 14px !important; margin-top: 8px !important; margin-bottom: 5px !important; }}
            p, ul, li {{ font-size: 12px !important; margin-top: 3px !important; margin-bottom: 3px !important; }}
            hr {{ margin: 8px 0 !important; border-top: 1px solid #ccc !important; }}
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

col_hdr1, col_hdr2, col_hdr3 = st.columns(3)
with col_hdr1: nome_commerciale = st.text_input("💼 Nome Commerciale INTEC:", placeholder="Es. Giovanni Rosano")
with col_hdr2: nome_cliente = st.text_input("👤 Nome Cliente / Cantiere:", placeholder="Es. Cantiere Navale Rossi")
with col_hdr3: data_offerta = st.date_input("📅 Data Offerta:", value=datetime.date.today(), format="DD/MM/YYYY")

commerciale_display = nome_commerciale if nome_commerciale else "Non specificato"
cliente_display = nome_cliente if nome_cliente else "Non specificato"
st.markdown(f"<div class='print-text' style='text-align: center;'><b>💼 Commerciale INTEC:</b> {commerciale_display} &nbsp;&nbsp;|&nbsp;&nbsp; <b>👤 Cliente/Cantiere:</b> {cliente_display} &nbsp;&nbsp;|&nbsp;&nbsp; <b>📅 Data:</b> {data_offerta.strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

st.markdown("---")

# 3. CONFIGURAZIONE PROGETTO
st.markdown("#### 1. Configurazione Progetto")
col_gen1, col_gen2, col_gen3, col_gen4 = st.columns(4)

with col_gen1: superficie = st.number_input("Superficie da trattare:", min_value=0.0, value=10.0, step=1.0)
with col_gen2: unita = st.selectbox("Unità di Misura:", ["Metri Quadri (m²)", "Piedi Quadri (sq ft)"])
with col_gen3: valuta = st.selectbox("Valuta:", ["Euro (€)", "Dollaro ($)"])
with col_gen4: tipo_applicazione = st.selectbox("Tipo di Applicazione:", ["Produzione Modello", "Lucidatura"])

# Calcolo superfici base
if unita == "Metri Quadri (m²)":
    superficie_m2 = superficie
    superficie_sqft = superficie * 10.7639
else:
    superficie_sqft = superficie
    superficie_m2 = superficie / 10.7639

is_us_market = (unita == "Piedi Quadri (sq ft)" and valuta == "Dollaro ($)")
valuta_simbolo = "$" if is_us_market else "€"
unita_peso_str = "lbs" if is_us_market else "kg"

st.markdown(f"<div class='print-text'><b>Superficie:</b> {superficie} {unita} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Valuta:</b> {valuta} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Applicazione:</b> {tipo_applicazione}</div>", unsafe_allow_html=True)
st.markdown("---")


# ==========================================
# PERCORSO A: PRODUZIONE MODELLO
# ==========================================
if tipo_applicazione == "Produzione Modello":
    st.markdown("#### 2. Analisi Comparativa Materiali e Tempi")
    col_intec, col_cliente = st.columns(2)

    moltiplicatori_r999 = {"MAT 300": 1.5, "MAT 450": 2.25, "OZ 1.0": 0.312, "OZ 1.5": 0.468}

    with col_intec:
        st.markdown("<h3 style='margin-bottom: 0px;'> <span style='display: inline-block; width: 15px; height: 15px; background-color: #008F99; border-radius: 50%; vertical-align: middle; margin-right: 5px;'></span>Sistema INTEC</h3>", unsafe_allow_html=True)
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1: prodotto_intec = st.selectbox("Prodotto:", ["PF07E", "PF07LS", "PF10E", "PF10GT", "PV10E"])
        with col_sel2: tipo_rinforzo = st.selectbox("Tipo di Rinforzo:", list(moltiplicatori_r999.keys()))
        
        if "MAT" in tipo_rinforzo:
            kg_r999 = superficie_m2 * moltiplicatori_r999[tipo_rinforzo]
        else: 
            kg_r999 = (superficie_sqft * moltiplicatori_r999[tipo_rinforzo]) / 2.20462  
            
        if is_us_market:
            display_r999 = kg_r999 * 2.20462
            unita_r999 = "lbs"
        else:
            display_r999 = kg_r999
            unita_r999 = "kg"
            
        if kg_r999 < 175.0:
            latte_r999 = kg_r999 / 25.0
            if is_us_market:
                testo_r999 = f"{display_r999:.2f} {unita_r999} [{latte_r999:.1f} pails (25 kg)] — *laminazione 2 strati*"
            else:
                testo_r999 = f"{display_r999:.2f} {unita_r999} [{latte_r999:.1f} latte (da 25 kg)] — *laminazione 2 strati*"
        else:
            fusti_r999 = kg_r999 / 225.0
            if is_us_market:
                testo_r999 = f"{display_r999:.2f} {unita_r999} [{fusti_r999*55.0:.1f} gallons / {fusti_r999:.1f} drums from 55 gal] — *laminazione 2 strati*"
            else:
                testo_r999 = f"{display_r999:.2f} {unita_r999} [{fusti_r999:.1f} fusti (da 225 kg)] — *laminazione 2 strati*"

        peso_specifico = 0.7 if "07" in prodotto_intec else 1.0
        consumo_m2 = 20.0 * peso_specifico
        peso_fusto = 200.0 * peso_specifico
        kg_prodotto = superficie_m2 * consumo_m2
        fusti_prodotto = kg_prodotto / peso_fusto 
        
        if is_us_market:
            testo_prodotto = f"{fusti_prodotto * 55.0:.1f} gallons ({fusti_prodotto:.1f} drums from 55 gal) — *thickness {16/25.4:.2f} inch*"
        else:
            testo_prodotto = f"{fusti_prodotto:.1f} fusti (da {peso_fusto:.0f} kg) — *spessore 16mm*"

        st.markdown(f"**Specifiche Tecniche:**\n- 📦 **{prodotto_intec}:** {testo_prodotto}\n- 🧪 **Resina R999 ({tipo_rinforzo}):** {testo_r999}")
        
        col_prezzi1, col_prezzi2 = st.columns(2)
        with col_prezzi1: prezzo_intec_input = st.number_input(f"Prezzo {prodotto_intec} ({valuta_simbolo}/{unita_peso_str}):", min_value=0.0, value=10.70, step=0.1)
        with col_prezzi2: prezzo_resina_input = st.number_input(f"Costo R999 ({valuta_simbolo}/{unita_peso_str}):", min_value=0.0, value=5.00, step=0.1)
        
        st.markdown(f"<div class='print-text'><b>Prezzi applicati dal venditore:</b><br>- {prodotto_intec}: {prezzo_intec_input:.2f} {valuta_simbolo}/{unita_peso_str}<br>- Resina R999: {prezzo_resina_input:.2f} {valuta_simbolo}/{unita_peso_str}</div>", unsafe_allow_html=True)
        
        # Conteggio ore pulito senza correttivi fissi (+2 rimosso)
        ore_intec = superficie_m2 / 5.0
        st.success(f"⏱️ Ore Manodopera Stimate: {ore_intec:.1f} h")
        
        costo_prodotto = (kg_prodotto * 2.20462 if is_us_market else kg_prodotto) * prezzo_intec_input
        costo_resina = (kg_r999 * 2.20462 if is_us_market else kg_r999) * prezzo_resina_input
        tot_generale_intec = costo_prodotto + costo_resina

    with col_cliente:
        st.markdown("<h3 style='margin-bottom: 0px;'> <span style='display: inline-block; width: 15px; height: 15px; background-color: #4A4A4A; border-radius: 50%; vertical-align: middle; margin-right: 5px;'></span>Metodo Attuale Cliente</h3>", unsafe_allow_html=True)
        tecnologia = st.selectbox("Tecnologia Concorrente:", ["Epossidica", "Spray"])
        col_q_cli1, col_q_cli2 = st.columns(2)
        with col_q_cli1: kg_cliente = st.number_input(f"Materiale Cliente ({unita_peso_str}):", min_value=0.0, value=0.0, step=10.0)
        with col_q_cli2: kg_resina_cliente = st.number_input(f"Resina Cliente ({unita_peso_str}):", min_value=0.0, value=0.0, step=10.0)
        col_p_cli1, col_p_cli2 = st.columns(2)
        with col_p_cli1: prezzo_cliente = st.number_input(f"Prezzo Mat. Cliente ({valuta_simbolo}/{unita_peso_str}):", min_value=0.0, value=0.0, step=0.5)
        with col_p_cli2: prezzo_resina_cliente = st.number_input(f"Prezzo Resina Cliente ({valuta_simbolo}/{unita_peso_str}):", min_value=0.0, value=0.0, step=0.5)
        
        ore_cliente = st.number_input(f"Ore totali cantiere Cliente:", min_value=0.0, value=0.0, step=1.0)
        st.markdown(f"<div class='print-text'><b>Tecnologia Cliente:</b> {tecnologia}<br>- Materiale Base: {kg_cliente:.1f} {unita_peso_str} <i>(a {prezzo_cliente:.2f} {valuta_simbolo}/{unita_peso_str})</i><br>- Resina: {kg_resina_cliente:.1f} {unita_peso_str} <i>(a {prezzo_resina_cliente:.2f} {valuta_simbolo}/{unita_peso_str})</i><br><b>Ore di lavoro previste:</b> {ore_cliente} h</div>", unsafe_allow_html=True)
        tot_generale_cliente = (kg_cliente * prezzo_cliente) + (kg_resina_cliente * prezzo_resina_cliente)

    st.markdown("---")
    st.markdown("#### 3. Impatto Visivo Risultati")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig_costi = go.Figure(go.Bar
