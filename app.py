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

# CSS AGGIORNATO: GESTIONE SPAZI E TESTI FANTASMA PER LA STAMPA SU SINGOLA PAGINA
st.markdown(f"""
    <style>
        .block-container {{ padding-top: 2.5rem !important; padding-bottom: 0.5rem !important; }}
        .logo-outer-container {{ display: flex; justify-content: center; width: 100%; margin-bottom: -10px; }}
        .logo-container {{ width: 380px; max-width: 100%; }}
        .logo-light {{ display: block; width: 100%; }}
        .logo-dark {{ display: none; width: 100%; }}
        
        /* TESTI FANTASMA: INVISIBILI A SCHERMO */
        .print-text {{ display: none; }}
        
        @media (prefers-color-scheme: dark) {{
            .logo-light {{ display: none; }}
            .logo-dark {{ display: block; }}
        }}
        
        @media print {{
            @page {{ margin: 0.3cm; size: A4 portrait; }} 
            
            /* NASCONDE I CAMPI DI INSERIMENTO IN STAMPA */
            .stButton, .stNumberInput, .stSelectbox, .stDateInput, .stTextInput, header[data-testid="stHeader"], [data-testid="stSidebar"] {{
                display: none !important;
            }}
            
            /* MOSTRA I TESTI FANTASMA SOLO IN STAMPA */
            .print-text {{ 
                display: block !important; 
                font-size: 11px !important; 
                margin-top: 2px !important; 
                margin-bottom: 6px !important; 
                line-height: 1.3 !important;
                color: black !important;
            }}
            
            .main, .block-container {{ background-color: white !important; color: black !important; padding: 0 !important; margin: 0 !important; }}
            .logo-dark {{ display: none !important; }}
            
            /* LOGO PIU' PICCOLO E SPAZI RIDOTTI */
            .logo-light {{ display: block !important; width: 160px !important; margin: 0 auto 2px auto !important; }}
            div[data-testid="column"] {{ width: 48% !important; flex: 1 1 48% !important; min-width: 48% !important; display: inline-block !important; vertical-align: top; }}
            div[data-testid="stMetric"] {{ padding: 0 !important; margin: 0 !important; }}
            div[data-testid="stAlert"] {{ padding: 4px 8px !important; margin-bottom: 2px !important; }}
            
            /* COMPRESSIONE TESTI */
            h3 {{ font-size: 14px !important; margin-top: 2px !important; margin-bottom: 2px !important; }}
            h4 {{ font-size: 12px !important; margin-top: 4px !important; margin-bottom: 2px !important; }}
            p, ul, li {{ margin-top: 1px !important; margin-bottom: 1px !important; padding: 0 !important; font-size: 11px !important; }}
            hr {{ margin: 3px 0 !important; border-top: 1px solid #ccc !important; }}
            
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

col_hdr1, col_hdr2, col_hdr3 = st.columns(3)
with col_hdr1:
    nome_commerciale = st.text_input("💼 Nome Commerciale INTEC:", placeholder="Es. Mario Rossi")
with col_hdr2:
    nome_cliente = st.text_input("👤 Nome Cliente / Cantiere:", placeholder="Es. Cantiere Navale Rossi")
with col_hdr3:
    data_offerta = st.date_input("📅 Data Offerta:", value=datetime.date.today(), format="DD/MM/YYYY")

# Testo fantasma intestazione (visibile solo in PDF)
commerciale_display = nome_commerciale if nome_commerciale else "Non specificato"
cliente_display = nome_cliente if nome_cliente else "Non specificato"
st.markdown(f"<div class='print-text' style='text-align: center; font-size: 12px;'><b>💼 Commerciale INTEC:</b> {commerciale_display} &nbsp;&nbsp;|&nbsp;&nbsp; <b>👤 Cliente/Cantiere:</b> {cliente_display} &nbsp;&nbsp;|&nbsp;&nbsp; <b>📅 Data:</b> {data_offerta.strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

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
    superficie = st.number_input("Superficie da trattare:", min_value=0.0, value=0.0, step=1.0)
with col_gen2:
    unita = st.selectbox("Unità di Misura:", ["Metri Quadri (m²)", "Piedi Quadri (sq ft)"])
with col_gen3:
    valuta = st.selectbox("Valuta:", ["Euro (€)", "Dollaro ($)"])

# Testo fantasma Configurazione
st.markdown(f"<div class='print-text'><b>Superficie:</b> {superficie} {unita} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Valuta:</b> {valuta}</div>", unsafe_allow_html=True)

st.markdown("---")

# 5. ANALISI COMPARATIVA
st.markdown("#### 2. Analisi Comparativa Materiali e Tempi")
col_intec, col_cliente = st.columns(2)

# Variabili per il controllo del Mercato USA e testi
is_us_market = (unita == "Piedi Quadri (sq ft)" and valuta == "Dollaro ($)")
valuta_simbolo = "$" if is_us_market else "€"
unita_peso_str = "lbs" if is_us_market else "kg"

# --- COLONNA INTEC ---
with col_intec:
    # Pallino Teal
    st.markdown("<h3 style='margin-bottom: 0px;'> <span style='display: inline-block; width: 15px; height: 15px; background-color: #008F99; border-radius: 50%; vertical-align: middle; margin-right: 5px;'></span>Sistema INTEC</h3>", unsafe_allow_html=True)
    
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
    
    # Calcolo resina R999 strutturale (Sempre in KG per la logica di soglia dei fusti)
    if "MAT" in tipo_rinforzo:
        kg_r999 = superficie_m2 * moltiplicatori_r999[tipo_rinforzo]
    else: 
        kg_r999 = (superficie_sqft * moltiplicatori_r999[tipo_rinforzo]) / 2.20462  
        
    # Conversione per la visualizzazione corretta (KG vs LBS)
    if is_us_market:
        display_r999 = kg_r999 * 2.20462
        unita_r999 = "lbs"
    else:
        display_r999 = kg_r999
        unita_r999 = "kg"
        
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
    
    # Formattazione condizionale
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
    
    # Testo fantasma prezzi INTEC
    st.markdown(f"""
    <div class='print-text'>
        <b>Prezzi applicati dal venditore:</b><br>
        - {prodotto_intec}: {prezzo_intec_input:.2f} {valuta_simbolo}/{unita_peso_str}<br>
        - Resina R999: {prezzo_resina_input:.2f} {valuta_simbolo}/{unita_peso_str}
    </div>
    """, unsafe_allow_html=True)
    
    ore_intec = (superficie_m2 / 5.0) + 2.0
    st.success(f"⏱️ Ore Manodopera Stimate: {ore_intec:.1f} h")
    
    # Calcolo totale economico separato INTEC
    if is_us_market:
        costo_prodotto = (kg_prodotto * 2.20462) * prezzo_intec_input
        costo_resina = (kg_r999 * 2.20462) * prezzo_resina_input
    else:
        costo_prodotto = kg_prodotto * prezzo_intec_input
        costo_resina = kg_r999 * prezzo_resina_input

    tot_generale_intec = costo_prodotto + costo_resina

# --- COLONNA CLIENTE ---
with col_cliente:
    # Pallino Grigio
    st.markdown("<h3 style='margin-bottom: 0px;'> <span style='display: inline-block; width: 15px; height: 15px; background-color: #4A4A4A; border-radius: 50%; vertical-align: middle; margin-right: 5px;'></span>Metodo Attuale Cliente</h3>", unsafe_allow_html=True)
    
    tecnologia = st.selectbox("Tecnologia Concorrente:", ["Epossidica", "Spray"])
    
    # Inserimento Quantità Separate Cliente
    col_q_cli1, col_q_cli2 = st.columns(2)
    with col_q_cli1:
        label_mat_cliente = "Materiale Cliente (lbs):" if is_us_market else "Materiale Cliente (KG):"
        kg_cliente = st.number_input(label_mat_cliente, min_value=0.0, value=0.0, step=10.0)
    with col_q_cli2:
        label_res_cliente = "Resina Cliente (lbs):" if is_us_market else "Resina Cliente (KG):"
        kg_resina_cliente = st.number_input(label_res_cliente, min_value=0.0, value=0.0, step=10.0)
    
    # Inserimento Prezzi Separati Cliente
    col_p_cli1, col_p_cli2 = st.columns(2)
    with col_p_cli1:
        label_prezzo_cliente = "Prezzo Mat. Cliente ($/lbs):" if is_us_market else "Prezzo Mat. Cliente (€/KG):"
        prezzo_cliente = st.number_input(label_prezzo_cliente, min_value=0.0, value=0.0, step=0.5)
    with col_p_cli2:
        label_prezzo_res_cliente = "Costo Resina Cliente ($/lbs):" if is_us_market else "Costo Resina Cliente (€/KG):"
        prezzo_resina_cliente = st.number_input(label_prezzo_res_cliente, min_value=0.0, value=0.0, step=0.5)
    
    ore_cliente = st.number_input(f"Ore totali cantiere Cliente:", min_value=0.0, value=0.0, step=1.0)
    
    # Testo fantasma dati CLIENTE
    st.markdown(f"""
    <div class='print-text'>
        <b>Tecnologia Cliente:</b> {tecnologia}<br>
        - Materiale Base: {kg_cliente:.1f} {unita_peso_str} <i>(a {prezzo_cliente:.2f} {valuta_simbolo}/{unita_peso_str})</i><br>
        - Resina: {kg_resina_cliente:.1f} {unita_peso_str} <i>(a {prezzo_resina_cliente:.2f} {valuta_simbolo}/{unita_peso_str})</i><br>
        <b>Ore di lavoro previste:</b> {ore_cliente} h
    </div>
    """, unsafe_allow_html=True)
    
    # Calcolo totale economico Cliente (Materiale + Resina)
    tot_generale_cliente = (kg_cliente * prezzo_cliente) + (kg_resina_cliente * prezzo_resina_cliente)

st.markdown("---")

# 6. GRAFICI
st.markdown("#### 3. Impatto Visivo Risultati")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    fig_costi = go.Figure()
    fig_costi.add_trace(go.Bar(
        x=['Sistema INTEC', 'Metodo Cliente'], y=[tot_generale_intec, tot_generale_cliente],
        marker_color=['#008F99', '#4A4A4A'],
        text=[f"{tot_generale_intec:,.2f} {valuta_simbolo}", f"{tot_generale_cliente:,.2f} {valuta_simbolo}"],
        textposition='auto', textfont=dict(color='white'), width=0.4
    ))
    fig_costi.update_layout(
        height=190, 
        title=dict(text="Costo Materiali", font=dict(size=13)), 
        yaxis=dict(showgrid=True),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        margin=dict(l=0, r=0, t=25, b=0)
    )
    st.plotly_chart(fig_costi, use_container_width=True, theme="streamlit", config={'staticPlot': True})

with col_chart2:
    fig_ore = go.Figure()
    fig_ore.add_trace(go.Bar(
        x=['Sistema INTEC', 'Metodo Cliente'], y=[ore_intec, ore_cliente],
        marker_color=['#008F99', '#4A4A4A'],
        text=[f"{ore_intec:.1f} h", f"{ore_cliente:.1f} h"],
        textposition='auto', textfont=dict(color='white'), width=0.4
    ))
    fig_ore.update_layout(
        height=190, 
        title=dict(text="Ore di Lavoro", font=dict(size=13)), 
        yaxis=dict(showgrid=True),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        margin=dict(l=0, r=0, t=25, b=0)
    )
    st.plotly_chart(fig_ore, use_container_width=True, theme="streamlit", config={'staticPlot': True})

# 7. BANNER FINALE E STAMPA
st.markdown("---")
risparmio_economico = tot_generale_cliente - tot_generale_intec
ore_risparmiate = ore_cliente - ore_intec

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label=f"TOTALE MATERIALI INTEC (IVA Incl.)", value=f"{tot_generale_intec:,.2f} {valuta_simbolo}")
with col_res2:
    st.metric(label=f"TOTALE MATERIALI CLIENTE (IVA Incl.)", value=f"{tot_generale_cliente:,.2f} {valuta_simbolo}")

if tot_generale_cliente > 0:
    st.success(f"💰 **Risparmio Netto sui Materiali:** {risparmio_economico:,.2f} {valuta_simbolo} | ⏱️ **Tempo Guadagnato:** {ore_risparmiate:.1f} ore")

st.markdown("---")
st.markdown("<p style='font-size: 11px; font-style: italic; margin-top: 0;'>⚠️ <b>Nota Tecnica:</b> I tempi di indurimento e fresabilità variano in base alla temperatura e alla catalisi.</p>", unsafe_allow_html=True)
