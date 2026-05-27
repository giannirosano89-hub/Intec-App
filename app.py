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

# CSS AGGIORNATO: GESTIONE STAMPA E BOX INFORMATIVI
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
            
            /* STILE BOX INFORMATIVI PER STAMPA */
            div[data-testid="stAlert"] {{ background-color: white !important; border: 2px solid #008F99 !important; padding: 10px !important; color: black !important; margin-bottom: 10px !important; }}
            div[data-testid="stAlert"] * {{ color: black !important; }}
            
            h3 {{ font-size: 16px !important; margin-top: 5px !important; margin-bottom: 5px !important; }}
            h4 {{ font-size: 14px !important; margin-top: 8px !important; margin-bottom: 5px !important; }}
            h5 {{ font-size: 13px !important; margin-top: 8px !important; margin-bottom: 4px !important; font-weight: bold; color: #008F99 !important; }}
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
col_gen1, col_gen2, col_gen3 = st.columns(3)

with col_gen1: superficie = st.number_input("Superficie da trattare:", min_value=0.0, value=10.0, step=1.0)
with col_gen2: unita = st.selectbox("Unità di Misura:", ["Metri Quadri (m²)", "Piedi Quadri (sq ft)"])
with col_gen3: valuta = st.selectbox("Valuta:", ["Euro (€)", "Dollaro ($)"])

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

st.markdown(f"<div class='print-text'><b>Superficie:</b> {superficie} {unita} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Valuta:</b> {valuta}</div>", unsafe_allow_html=True)
st.markdown("---")

# 4. ANALISI COMPARATIVA
st.markdown("#### 2. Analisi Comparativa: Produzione Modello")
col_intec, col_cliente = st.columns(2)

moltiplicatori_r999 = {"MAT 300": 1.5, "MAT 450": 2.25, "OZ 1.0": 0.312, "OZ 1.5": 0.468}

# --- COLONNA INTEC ---
with col_intec:
    st.markdown("<h3 style='margin-bottom: 0px;'> <span style='display: inline-block; width: 15px; height: 15px; background-color: #008F99; border-radius: 50%; vertical-align: middle; margin-right: 5px;'></span>Sistema INTEC</h3>", unsafe_allow_html=True)
    
    # ---------------- FASE 1: RESINA ----------------
    st.markdown("##### 🧪 1. Laminazione R999")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        tipo_rinforzo = st.selectbox("Tipo di Rinforzo:", list(moltiplicatori_r999.keys()))
    with col_r2:
        prezzo_resina_input = st.number_input(f"Prezzo R999 ({valuta_simbolo}/{unita_peso_str}):", min_value=0.0, value=5.00, step=0.1)
    
    if "MAT" in tipo_rinforzo:
        kg_r999 = superficie_m2 * moltiplicatori_r999[tipo_rinforzo]
    else: 
        kg_r999 = (superficie_sqft * moltiplicatori_r999[tipo_rinforzo]) / 2.20462  
        
    display_r999 = kg_r999 * 2.20462 if is_us_market else kg_r999
    unita_r999 = "lbs" if is_us_market else "kg"
        
    if kg_r999 < 175.0:
        latte_r999 = kg_r999 / 25.0
        testo_log_r999 = f"[{latte_r999:.1f} {'pails (25 kg)' if is_us_market else 'latte (da 25 kg)'}]"
    else:
        fusti_r999 = kg_r999 / 225.0
        testo_log_r999 = f"[{fusti_r999*55.0:.1f} gallons / {fusti_r999:.1f} drums from 55 gal]" if is_us_market else f"[{fusti_r999:.1f} fusti (da 225 kg)]"

    testo_r999 = f"{display_r999:.2f} {unita_r999} {testo_log_r999} — *laminazione 2 strati*"
    ore_r999_base = superficie_m2 * (20.0 / 60.0)
    
    st.info(f"**Specifiche Laminazione:**\n- 🧪 **R999 ({tipo_rinforzo}):** {testo_r999}\n- ⏱️ **Manodopera:** {ore_r999_base:.1f} h *(calcolo: 1 m² = 20 min)*")


    # ---------------- FASE 2: PASTE ----------------
    st.markdown("##### 📦 2. Applicazione Paste")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        prodotto_intec = st.selectbox("Prodotto Base:", ["PF07E", "PF07LS", "PF10E", "PF10GT", "PV10E"])
    with col_p2:
        prezzo_intec_input = st.number_input(f"Prezzo {prodotto_intec} ({valuta_simbolo}/{unita_peso_str}):", min_value=0.0, value=10.70, step=0.1)
        
    peso_specifico = 0.7 if "07" in prodotto_intec else 1.0
    kg_prodotto = superficie_m2 * (20.0 * peso_specifico)
    fusti_prodotto = kg_prodotto / (200.0 * peso_specifico)
    
    if is_us_market:
        testo_prodotto = f"{fusti_prodotto * 55.0:.1f} gallons ({fusti_prodotto:.1f} drums from 55 gal) — *thickness {16/25.4:.2f} inch*"
    else:
        testo_prodotto = f"{fusti_prodotto:.1f} fusti (da {200.0 * peso_specifico:.0f} kg) — *spessore 16mm*"

    ore_paste_base = superficie_m2 / 5.0
    
    st.info(f"**Specifiche Paste:**\n- 📦 **{prodotto_intec}:** {testo_prodotto}\n- ⏱️ **Manodopera:** {ore_paste_base:.1f} h *(calcolo: 5 m² = 1 ora)*")


    # ---------------- FASE 3: TOTALI MANODOPERA ----------------
    st.markdown("##### ⏱️ 3. Riepilogo Manodopera INTEC")
    col_o1, col_o2 = st.columns(2)
    
    with col_o1: 
        ore_totali_intec = st.number_input("Ore totali (R999 + Paste):", min_value=0.0, value=float(ore_r999_base + ore_paste_base), step=0.5)
    with col_o2: 
        costo_orario_intec = st.number_input(f"Tariffa INTEC ({valuta_simbolo}/h):", min_value=0.0, value=35.0, step=1.0)
        
    # STAMPA FANTASMA INTEC PREZZI E ORE
    st.markdown(f"""
    <div class='print-text'><b>Dati Economici INTEC (Prezzi e Ore Inserite):</b><br>
    - Resina R999: {prezzo_resina_input:.2f} {valuta_simbolo}/{unita_peso_str}<br>
    - Pasta {prodotto_intec}: {prezzo_intec_input:.2f} {valuta_simbolo}/{unita_peso_str}<br>
    - Manodopera Totale: {ore_totali_intec:.1f} h (a {costo_orario_intec:.2f} {valuta_simbolo}/h)
    </div>
    """, unsafe_allow_html=True)
    
    # Calcolo Costi finali INTEC
    costo_mat_intec = (kg_r999 * 2.20462 if is_us_market else kg_r999) * prezzo_resina_input + \
                      (kg_prodotto * 2.20462 if is_us_market else kg_prodotto) * prezzo_intec_input
    costo_manodopera_intec = ore_totali_intec * costo_orario_intec
    tot_generale_intec = costo_mat_intec + costo_manodopera_intec

    # RIEPILOGO TOTALE DI COLONNA
    st.success(f"**RIEPILOGO INTEC**\n- ⏱️ Ore Totali: {ore_totali_intec:.1f} h\n- 💰 Costo Totale: {tot_generale_intec:,.2f} {valuta_simbolo}")

# --- COLONNA CLIENTE ---
with col_cliente:
    st.markdown("<h3 style='margin-bottom: 0px;'> <span style='display: inline-block; width: 15px; height: 15px; background-color: #4A4A4A; border-radius: 50%; vertical-align: middle; margin-right: 5px;'></span>Metodo Attuale Cliente</h3>", unsafe_allow_html=True)
    
    st.markdown("##### 🛠️ 1. Dati Economici e Manodopera")
    tecnologia = st.selectbox("Tecnologia Concorrente:", ["Epossidica", "Duratec"])
    
    costo_mat_cliente = st.number_input(f"Costo Totale Materiale ({valuta_simbolo}):", min_value=0.0, value=0.0, step=10.0)
    
    col_c_o1, col_c_o2 = st.columns(2)
    with col_c_o1:
        ore_cliente = st.number_input(f"Ore totali previste:", min_value=0.0, value=0.0, step=1.0)
    with col_c_o2:
        costo_orario_cliente = st.number_input(f"Tariffa Cliente ({valuta_simbolo}/h):", min_value=0.0, value=35.0, step=1.0)
    
    # STAMPA FANTASMA CLIENTE
    st.markdown(f"""
    <div class='print-text'><b>Dati Inseriti Cliente ({tecnologia}):</b><br>
    - Costo Totale Materiale: {costo_mat_cliente:.2f} {valuta_simbolo}<br>
    - Manodopera Totale: {ore_cliente:.1f} h (a {costo_orario_cliente:.2f} {valuta_simbolo}/h)
    </div>
    """, unsafe_allow_html=True)
    
    # Calcolo Totali Cliente
    costo_manodopera_cliente = ore_cliente * costo_orario_cliente
    tot_generale_cliente = costo_mat_cliente + costo_manodopera_cliente

    # RIEPILOGO TOTALE DI COLONNA
    st.info(f"**RIEPILOGO CLIENTE**\n- ⏱️ Ore Totali: {ore_cliente:.1f} h\n- 💰 Costo Totale: {tot_generale_cliente:,.2f} {valuta_simbolo}")

st.markdown("---")

# 5. GRAFICI
st.markdown("#### 3. Impatto Visivo Risultati")

col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    fig_costi = go.Figure(go.Bar(
        x=['Sistema INTEC', 'Metodo Cliente'], y=[tot_generale_intec, tot_generale_cliente],
        marker_color=['#008F99', '#4A4A4A'],
        text=[f"{tot_generale_intec:,.2f} {valuta_simbolo}", f"{tot_generale_cliente:,.2f} {valuta_simbolo}"],
        textposition='auto', textfont=dict(color='white'), width=0.35
    ))
    fig_costi.update_layout(height=220, title=dict(text="Costo Finale Reale (Mat. + Lavoro)", font=dict(size=13)), margin=dict(l=10, r=40, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_costi, use_container_width=True, theme="streamlit", config={'staticPlot': True})

with col_chart2:
    fig_ore = go.Figure(go.Bar(
        x=['Sistema INTEC', 'Metodo Cliente'], y=[ore_totali_intec, ore_cliente],
        marker_color=['#008F99', '#4A4A4A'],
        text=[f"{ore_totali_intec:.1f} h", f"{ore_cliente:.1f} h"],
        textposition='auto', textfont=dict(color='white'), width=0.35
    ))
    fig_ore.update_layout(height=220, title=dict(text="Ore Totali di Lavoro", font=dict(size=13)), margin=dict(l=10, r=40, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_ore, use_container_width=True, theme="streamlit", config={'staticPlot': True})

# 6. BANNER RISPARMIO E STAMPA
st.markdown("---")
risparmio_economico = tot_generale_cliente - tot_generale_intec
ore_risparmiate = ore_cliente - ore_totali_intec

if tot_generale_cliente > 0:
    if risparmio_economico >= 0:
        st.success(f"💰 **Risparmio Netto Totale (Mat. + Lavoro):** {risparmio_economico:,.2f} {valuta_simbolo} | ⏱️ **Tempo Guadagnato:** {ore_risparmiate:.1f} ore")
    else:
        st.error(f"📉 **Differenza Costi (Mat. + Lavoro):** {risparmio_economico:,.2f} {valuta_simbolo} | ⏱️ **Differenza Ore:** {ore_risparmiate:.1f} ore")

st.markdown("---")
st.markdown("<p style='font-size: 11px; font-style: italic; margin-top: 0;'>⚠️ <b>Nota Tecnica:</b> I tempi di indurimento e fresabilità variano in base alla temperatura e alla catalisi. I costi esposti sommano materiale e manodopera.</p>", unsafe_allow_html=True)
