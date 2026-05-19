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

# CSS Avanzato per Spazi, Centratura e STAMPA PULITA in 1 Pagina
st.markdown(f"""
    <style>
        /* 1. Sposta tutto più in alto rimuovendo lo spazio vuoto di Streamlit */
        .block-container {{
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
        }}
        
        /* 2. Centratura Logo e Gestione Tema Mobile */
        .logo-outer-container {{ display: flex; justify-content: center; width: 100%; margin-bottom: 10px; }}
        .logo-container {{ width: 450px; max-width: 100%; }}
        .logo-light {{ display: block; width: 100%; }}
        .logo-dark {{ display: none; width: 100%; }}
        
        @media (prefers-color-scheme: dark) {{
            .logo-light {{ display: none; }}
            .logo-dark {{ display: block; }}
        }}
        
        /* 3. Ottimizzazione STAMPA: Forza colori, margini compatti e nasconde gli input */
        @media print {{
            @page {{ margin: 0.5cm; size: A4 portrait; }} 
            
            .stButton, .stNumberInput, .stSelectbox, .stDateInput, .stTextInput, header, [data-testid="stSidebar"] {{
                display: none !important;
            }}
            
            /* Sfondo bianco assoluto per risparmiare inchiostro/PDF pulito */
            .main, .block-container {{ background-color: white !important; color: black !important; padding: 0 !important; }}
            
            /* Forza il logo chiaro rimpicciolito */
            .logo-dark {{ display: none !important; }}
            .logo-light {{ display: block !important; width: 250px !important; margin: 0 auto 5px auto !important; }}
            
            /* Riduce le spaziature per far entrare tutto in un foglio */
            h3, h4 {{ margin-top: 5px !important; margin-bottom: 5px !important; padding: 0 !important; font-size: 14px !important; }}
            hr {{ margin: 5px 0 !important; }}
            
            /* TRUCCO MAGICO: Forza il testo dei grafici a nero durante la stampa se l'utente era in Dark Mode */
            .js-plotly-plot .plotly text {{
                fill: #000000 !important;
            }}
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
st.markdown("<h3 style='text-align: center;'>Calcolatore di Efficienza e ROI — Supporto alla Vendita</h3>", unsafe_allow_html=True)

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

# --- COLONNA INTEC ---
with col_intec:
    st.subheader("🟢 Sistema INTEC")
    tipo_rinforzo = st.selectbox("Tipo di Rinforzo:", ["MAT 300", "MAT 450", "OZ 6", "OZ 10"])
    
    # Dizionario Moltiplicatori 
    moltiplicatori_r999 = {"MAT 300": 0.350, "MAT 450": 0.468, "OZ 6": 0.600, "OZ 10": 1.000}
    
    kg_r999 = superficie * moltiplicatori_r999[tipo_rinforzo]
    kg_pf07e = superficie * 14.0
    fusti_pf07e = kg_pf07e / 140.0 
    kg_tot_intec = kg_pf07e + kg_r999
    
    st.markdown(f"""
    **Specifiche Tecniche:**
    - 📦 **PF07E:** {fusti_pf07e:.1f} fusti (da 140 kg) — *spessore 16mm*
    - 🧪 **Resina R999 ({tipo_rinforzo}):** {kg_r999:.2f} kg — *laminazione 2 strati*
    """)
    
    prezzo_intec_input = st.number_input("Prezzo Materiale INTEC (Medio €/KG):", min_value=0.0, value=10.70, step=0.1)
    
    ore_intec = (superficie / 5.0) + 2.0
    st.success(f"⏱️ Ore Manodopera Stimate: {ore_intec:.1f} h")
    tot_generale_intec = kg_tot_intec * prezzo_intec_input

# --- COLONNA CLIENTE ---
with col_cliente:
    st.subheader("⚪ Metodo Attuale Cliente")
    tecnologia = st.selectbox("Tecnologia Concorrente:", ["Epossidica", "Spray", "Laminazione Manuale"])
    kg_cliente = st.number_input(f"Totale materiale Cliente (KG):", min_value=0.0, value=0.0, step=10.0)
    prezzo_cliente = st.number_input(f"Prezzo al KG Cliente:", min_value=0.0, value=0.0, step=0.5)
    ore_cliente = st.number_input(f"Ore totali cantiere Cliente:", min_value=0.0, value=0.0, step=1.0)
    tot_generale_cliente = kg_cliente * prezzo_cliente

st.markdown("---")

# 6. GRAFICI
st.markdown("#### 3. Impatto Visivo Risultati")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    fig_costi = go.Figure()
    fig_costi.add_trace(go.Bar(
        x=['Sistema INTEC', 'Metodo Cliente'], y=[tot_generale_intec, tot_generale_cliente],
        marker_color=['#008F99', '#4A4A4A'],
        text=[f"{tot_generale_intec:,.2f} {valuta}", f"{tot_generale_cliente:,.2f} {valuta}"],
        textposition='auto', textfont=dict(color='white'), width=0.4
    ))
    fig_costi.update_layout(
        title=dict(text="Costo Materiali", font=dict(size=14)), 
        yaxis=dict(showgrid=True),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        margin=dict(l=0, r=0, t=30, b=0) # Margini compatti
    )
    # L'argomento config={'staticPlot': True} BLOCCA l'interazione da mobile (niente zoom o swipe)
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
        title=dict(text="Ore di Lavoro", font=dict(size=14)), 
        yaxis=dict(showgrid=True),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        margin=dict(l=0, r=0, t=30, b=0)
    )
    # Blocco interazione da mobile
    st.plotly_chart(fig_ore, use_container_width=True, theme="streamlit", config={'staticPlot': True})

# 7. BANNER FINALE E STAMPA
st.markdown("---")
risparmio_economico = tot_generale_cliente - tot_generale_intec
ore_risparmiate = ore_cliente - ore_intec

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label="TOTALE MATERIALI INTEC (IVA Incl.)", value=f"{tot_generale_intec:,.2f} {valuta}")
with col_res2:
    st.metric(label="TOTALE MATERIALI CLIENTE (IVA Incl.)", value=f"{tot_generale_cliente:,.2f} {valuta}")

if tot_generale_cliente > 0:
    st.success(f"💰 **Risparmio Netto sui Materiali:** {risparmio_economico:,.2f} {valuta} | ⏱️ **Tempo Guadagnato:** {ore_risparmiate:.1f} ore")

st.markdown("---")
st.markdown("⚠️ **Nota Tecnica:** *I tempi di indurimento e fresabilità variano in base alla temperatura e alla catalisi.*")
