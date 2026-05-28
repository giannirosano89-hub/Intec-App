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

# CSS: GESTIONE STAMPA E ALLINEAMENTO BOX
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
            
            .stPlotlyChart {{ width: 330px !important; margin: 0 auto !important; display: block !important; }}
            
            div[data-testid="column"] {{ width: 48% !important; flex: 1 1 48% !important; display: inline-block !important; vertical-align: top; }}
            div[data-testid="stMetric"] {{ padding: 0 !important; margin: 0 !important; }}
            
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

is_dollar = (valuta == "Dollaro ($)")
is_sqft = (unita == "Piedi Quadri (sq ft)")

valuta_simbolo = "$" if is_dollar else "€"
unita_peso_str = "lbs" if is_sqft else "kg"

st.markdown(f"<div class='print-text'><b>Superficie:</b> {superficie} {unita} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Valuta:</b> {valuta}</div>", unsafe_allow_html=True)
st.markdown("---")

moltiplicatori_r999 = {"MAT 300": 1.5, "MAT 450": 2.25, "OZ 1.0": 0.312, "OZ 1.5": 0.468}


# ==========================================
# FASE 1: LAMINAZIONE RESINA
# ==========================================
st.markdown("#### 2. Fase 1: Laminazione Resina")
col_r_int, col_r_cli = st.columns(2)

# --- FASE 1: INTEC ---
with col_r_int:
    st.markdown("##### <span style='color:#008F99;'>🟢 Sistema INTEC (R999)</span>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <label style="font-size: 14px; display: block; margin-bottom: 0.5rem; color: inherit;">Tecnologia INTEC:</label>
            <div style="height: 39px; display: flex; align-items: center; background-color: rgba(128, 128, 128, 0.1); border-radius: 8px; padding: 0 12px; border: 1px solid rgba(128, 128, 128, 0.2); font-size: 14px;">
                <b>🛠️ Intec R999</b> &nbsp;|&nbsp; <b>⚖️ Rapporto impregnazione:</b> 1:2,5
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_i_row2_1, col_i_row2_2 = st.columns(2)
    with col_i_row2_1:
        metodo_app_intec = st.selectbox("Metodo di Applicazione INTEC:", ["Applicazione manuale", "Applicazione con taglio e spruzzo"])
    with col_i_row2_2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        st.text("Resa calcolata automaticamente")
    
    is_spray_intec = (metodo_app_intec == "Applicazione con taglio e spruzzo")
    
    col_i_row3_1, col_i_row3_2 = st.columns(2)
    with col_i_row3_1:
        tipo_rinforzo = st.selectbox("Tipo di Rinforzo INTEC:", list(moltiplicatori_r999.keys()), disabled=is_spray_intec)
    with col_i_row3_2:
        prezzo_resina_input = st.number_input(f"Prezzo R999 ({valuta_simbolo}/{unita_peso_str}):", min_value=0.0, value=5.00, step=0.1)
    
    if "MAT" in tipo_rinforzo:
        kg_r999 = superficie_m2 * moltiplicatori_r999[tipo_rinforzo]
    else: 
        kg_r999 = (superficie_sqft * moltiplicatori_r999[tipo_rinforzo]) / 2.20462  
        
    display_r999 = kg_r999 * 2.20462 if is_sqft else kg_r999
    testo_r999 = f"{display_r999:.2f} {unita_peso_str} — *laminazione 2 strati*"
    
    if is_spray_intec:
        ore_r999_base = round(superficie_m2 * (2.0 / 60.0), 2)
    else:
        ore_r999_base = round(superficie_m2 * (20.0 / 60.0), 2)
        
    col_i_row4_1, col_i_row4_2 = st.columns(2)
    with col_i_row4_1:
        ore_r999_intec = st.number_input("Ore manodopera INTEC:", min_value=0.0, value=float(ore_r999_base), step=0.5)
    with col_i_row4_2:
        costo_orario_r_intec = st.number_input(f"Tariffa Lavoro INTEC ({valuta_simbolo}/h):", min_value=0.0, value=35.0, step=1.0)
    
    costo_mat_r_intec = (kg_r999 * 2.20462 if is_sqft else kg_r999) * prezzo_resina_input
    costo_mano_r_intec = ore_r999_intec * costo_orario_r_intec
    tot_fase1_intec = costo_mat_r_intec + costo_mano_r_intec
    
    rinforzo_intec_display = "N/D (Spruzzo)" if is_spray_intec else tipo_rinforzo
    st.info(f"""**Specifiche Laminazione:**
- 🛠️ **Tecnologia:** Intec R999 ({metodo_app_intec})
- 🧶 **Rinforzo:** {rinforzo_intec_display}
- 🧪 **Resa R999:** {testo_r999}
- ⏱️ **Manodopera:** {ore_r999_intec:.1f} h *(1 persona sola)*""")
    
    st.markdown(f"<div class='print-text'><b>Fase 1 INTEC:</b><br>- Metodo: {metodo_app_intec}<br>- Rinforzo: {rinforzo_intec_display}<br>- R999: {prezzo_resina_input:.2f} {valuta_simbolo}/{unita_peso_str}<br>- Ore: {ore_r999_intec:.1f} h (a {costo_orario_r_intec:.2f} {valuta_simbolo}/h)<br>- Subtotale: {tot_fase1_intec:.2f} {valuta_simbolo}</div>", unsafe_allow_html=True)
    st.success(f"**Subtotale Fase 1 (INTEC):** {tot_fase1_intec:,.2f} {valuta_simbolo}")

# --- FASE 1: CLIENTE ---
with col_r_cli:
    st.markdown("##### <span style='color:#4A4A4A;'>⚪ Metodo Cliente (Resina)</span>", unsafe_allow_html=True)
    tecnologia_r_cliente = st.selectbox("Tecnologia Concorrente Resina:", ["Epossidica", "Duratec"])
    
    col_c_row2_1, col_c_row2_2 = st.columns(2)
    with col_c_row2_1:
        metodo_app_cliente = st.selectbox("Metodo di Applicazione Cliente:", ["Applicazione manuale", "Applicazione con taglio e spruzzo"])
    with col_c_row2_2:
        quantita_r_cliente = st.number_input(f"Quantità Utilizzata Resina ({unita_peso_str}):", min_value=0.0, value=0.0, step=1.0)
    
    is_spray_cliente = (metodo_app_cliente == "Applicazione con taglio e spruzzo")
    
    col_c_row3_1, col_c_row3_2 = st.columns(2)
    with col_c_row3_1:
        tipo_rinforzo_cliente = st.selectbox("Tipo di Rinforzo Cliente:", list(moltiplicatori_r999.keys()), disabled=is_spray_cliente)
    with col_c_row3_2:
        prezzo_r_cliente = st.number_input(f"Prezzo Resina Cliente ({valuta_simbolo}/{unita_peso_str}):", min_value=0.0, value=0.0, step=0.1)
    
    col_c_row4_1, col_c_row4_2 = st.columns(2)
    with col_c_row4_1:
        ore_r_cliente = st.number_input(f"Ore necessarie Resina:", min_value=0.0, value=0.0, step=1.0)
    with col_c_row4_2:
        costo_orario_r_cliente = st.number_input(f"Tariffa Lavoro Cliente Resina ({valuta_simbolo}/h):", min_value=0.0, value=35.0, step=1.0)
    
    costo_mat_r_cliente = quantita_r_cliente * prezzo_r_cliente
    costo_mano_r_cliente = ore_r_cliente * costo_orario_r_cliente
    tot_fase1_cliente = costo_mat_r_cliente + costo_mano_r_cliente
    
    rinforzo_cliente_display = "N/D (Spruzzo)" if is_spray_cliente else tipo_rinforzo_cliente
    st.info(f"""**Specifiche Laminazione:**
- 🛠️ **Tecnologia:** {tecnologia_r_cliente} ({metodo_app_cliente})
- 🧶 **Rinforzo:** {rinforzo_cliente_display}
- 🧪 **Resa Materiale:** {quantita_r_cliente:.2f} {unita_peso_str}
- ⏱️ **Manodopera:** {ore_r_cliente:.1f} h *(1 persona sola)*""")
    
    st.markdown(f"<div class='print-text'><b>Fase 1 Cliente ({tecnologia_r_cliente}):</b><br>- Metodo: {metodo_app_cliente}<br>- Rinforzo: {rinforzo_cliente_display}<br>- Quantità: {quantita_r_cliente:.2f} {unita_peso_str}<br>- Costo Mat.: {costo_mat_r_cliente:.2f} {valuta_simbolo}<br>- Ore: {ore_r_cliente:.1f} h (a {costo_orario_r_cliente:.2f} {valuta_simbolo}/h)<br>- Subtotale: {tot_fase1_cliente:.2f} {valuta_simbolo}</div>", unsafe_allow_html=True)
    st.info(f"**Subtotale Fase 1 (Cliente):** {tot_fase1_cliente:,.2f} {valuta_simbolo}")

st.markdown("---")


# ==========================================
# FASE 2: APPLICAZIONE PASTE
# ==========================================
st.markdown("#### 3. Fase 2: Applicazione Paste")
col_p_int, col_p_cli = st.columns(2)

# --- FASE 2: INTEC ---
with col_p_int:
    st.markdown("##### <span style='color:#008F99;'>🟢 Sistema INTEC (Paste)</span>", unsafe_allow_html=True)
    prodotto_intec = st.selectbox("Prodotto Base:", ["PF07E", "PF07LS", "PF10E", "PF10GT", "PV10E"])
    
    # Box di testo simulato per pareggiare perfettamente il menu a tendina "Metodo" del Cliente
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <div style="height: 39px; display: flex; align-items: center; background-color: rgba(128, 128, 128, 0.1); border-radius: 8px; padding: 0 12px; border: 1px solid rgba(128, 128, 128, 0.2); font-size: 14px;">
                <b>🛠️ Metodo Applicazione INTEC:</b> &nbsp; Estrusione
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    peso_specifico = 0.7 if "07" in prodotto_intec else 1.0
    kg_prodotto = superficie_m2 * (20.0 * peso_specifico)
    fusti_prodotto = kg_prodotto / (200.0 * peso_specifico)
    
    if is_sqft:
        testo_prodotto = f"{fusti_prodotto * 55.0:.1f} gallons ({fusti_prodotto:.1f} drums from 55 gal) — *thickness {16/25.4:.2f} inch*"
    else:
        testo_prodotto = f"{fusti_prodotto:.1f} fusti (da {200.0 * peso_specifico:.0f} kg) — *spessore 16mm*"
    
    col_prezzi_p1, col_prezzi_p2 = st.columns(2)
    with col_prezzi_p1:
        prezzo_pasta_input = st.number_input(f"Prezzo {prodotto_intec} ({valuta_simbolo}/{unita_peso_str}):", min_value=0.0, value=10.70, step=0.1)
    with col_prezzi_p2:
        costo_orario_p_intec = st.number_input(f"Tariffa Lavoro Paste ({valuta_simbolo}/h):", min_value=0.0, value=35.0, step=1.0)
        
    ore_paste_base = round(superficie_m2 / 5.0, 2)
    ore_paste_intec = st.number_input("Ore manodopera Paste INTEC:", min_value=0.0, value=float(ore_paste_base), step=0.5)

    costo_mat_p_intec = (kg_prodotto * 2.20462 if is_sqft else kg_prodotto) * prezzo_pasta_input
    costo_mano_p_intec = ore_paste_intec * costo_orario_p_intec
    tot_fase2_intec = costo_mat_p_intec + costo_mano_p_intec
    
    st.info(f"""**Specifiche Paste:**
- 📦 **Prodotto:** {prodotto_intec}
- 📐 **Volume Stimato:** {testo_prodotto}
- ⏱️ **Manodopera:** {ore_paste_intec:.1f} h *(1 persona sola)*""")
    
    st.markdown(f"<div class='print-text'><b>Fase 2 INTEC:</b><br>- Pasta {prodotto_intec}: {prezzo_pasta_input:.2f} {valuta_simbolo}/{unita_peso_str}<br>- Ore: {ore_paste_intec:.1f} h (a {costo_orario_p_intec:.2f} {valuta_simbolo}/h)<br>- Subtotale: {tot_fase2_intec:.2f} {valuta_simbolo}</div>", unsafe_allow_html=True)
    st.success(f"**Subtotale Fase 2 (INTEC):** {tot_fase2_intec:,.2f} {valuta_simbolo}")

# --- FASE 2: CLIENTE ---
with col_p_cli:
    st.markdown("##### <span style='color:#4A4A4A;'>⚪ Metodo Cliente (Paste)</span>", unsafe_allow_html=True)
    tecnologia_p_cliente = st.selectbox("Tecnologia Concorrente Paste:", ["Epossidica", "Spraycore"])
    
    metodo_p_cliente = st.selectbox("Metodo Applicazione Paste Cliente:", ["Applicazione manuale", "Applicazione con taglio e spruzzo"])
    
    col_c_op1, col_c_op2 = st.columns(2)
    with col_c_op1:
        costo_mat_p_cliente = st.number_input(f"Costo Totale Materiale Paste ({valuta_simbolo}):", min_value=0.0, value=0.0, step=10.0)
    with col_c_op2:
        costo_orario_p_cliente = st.number_input(f"Tariffa Lavoro Paste Cliente ({valuta_simbolo}/h):", min_value=0.0, value=35.0, step=1.0)
        
    ore_p_cliente = st.number_input("Ore necessarie Paste:", min_value=0.0, value=0.0, step=1.0)
        
    costo_mano_p_cliente = ore_p_cliente * costo_orario_p_cliente
    tot_fase2_cliente = costo_mat_p_cliente + costo_mano_p_cliente
    
    st.info(f"""**Specifiche Applicazione Paste:**
- 🛠️ **Tecnologia:** {tecnologia_p_cliente} ({metodo_p_cliente})
- ⏱️ **Manodopera:** {ore_p_cliente:.1f} h *(1 persona sola)*""")
    
    st.markdown(f"<div class='print-text'><b>Fase 2 Cliente ({tecnologia_p_cliente}):</b><br>- Costo Mat.: {costo_mat_p_cliente:.2f} {valuta_simbolo}<br>- Ore: {ore_p_cliente:.1f} h (a {costo_orario_p_cliente:.2f} {valuta_simbolo}/h)<br>- Subtotale: {tot_fase2_cliente:.2f} {valuta_simbolo}</div>", unsafe_allow_html=True)
    st.info(f"**Subtotale Fase 2 (Cliente):** {tot_fase2_cliente:,.2f} {valuta_simbolo}")

st.markdown("---")

# ==========================================
# AGGREGAZIONE TOTALI E GRAFICI
# ==========================================
ore_totali_intec = ore_r999_intec + ore_paste_intec
tot_generale_intec = tot_fase1_intec + tot_fase2_intec

ore_totali_cliente = ore_r_cliente + ore_p_cliente
tot_generale_cliente = tot_fase1_cliente + tot_fase2_cliente

st.markdown("#### 4. Riepilogo Finale (Laminazione + Paste)")

col_res1, col_res2, col_res3, col_res4 = st.columns(4)
with col_res1: st.metric(label="⏱️ ORE TOTALI INTEC", value=f"{ore_totali_intec:.1f} h")
with col_res2: st.metric(label="⏱️ ORE TOTALI CLIENTE", value=f"{ore_totali_cliente:.1f} h")
with col_res3: st.metric(label=f"💰 COSTO TOTALE INTEC", value=f"{tot_generale_intec:,.2f} {valuta_simbolo}")
with col_res4: st.metric(label=f"💰 COSTO TOTALE CLIENTE", value=f"{tot_generale_cliente:,.2f} {valuta_simbolo}")

st.markdown("<br>", unsafe_allow_html=True)

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
        x=['Sistema INTEC', 'Metodo Cliente'], y=[ore_totali_intec, ore_totali_cliente],
        marker_color=['#008F99', '#4A4A4A'],
        text=[f"{ore_totali_intec:.1f} h", f"{ore_totali_cliente:.1f} h"],
        textposition='auto', textfont=dict(color='white'), width=0.35
    ))
    fig_ore.update_layout(height=220, title=dict(text="Ore Totali di Lavoro", font=dict(size=13)), margin=dict(l=10, r=40, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_ore, use_container_width=True, theme="streamlit", config={'staticPlot': True})

# 6. BANNER RISPARMIO E STAMPA
st.markdown("---")
risparmio_economico = tot_generale_cliente - tot_generale_intec
ore_risparmiate = ore_totali_cliente - ore_totali_intec

if tot_generale_cliente > 0:
    if risparmio_economico >= 0:
        st.success(f"💰 **Risparmio Netto Totale (Mat. + Lavoro):** {risparmio_economico:,.2f} {valuta_simbolo} | ⏱️ **Tempo Guadagnato:** {ore_risparmiate:.1f} ore")
    else:
        st.error(f"📉 **Differenza Costi (Mat. + Lavoro):** {risparmio_economico:,.2f} {valuta_simbolo} | ⏱️ **Differenza Ore:** {ore_risparmiate:.1f} ore")

st.markdown("---")
st.markdown("<p style='font-size: 11px; font-style: italic; margin-top: 0;'>⚠️ <b>Nota Tecnica:</b> I tempi di indurimento e fresabilità variano in base alla temperatura e alla catalisi. I costi esposti sommano materiale e manodopera calcolati per tutte le fasi.</p>", unsafe_allow_html=True)
