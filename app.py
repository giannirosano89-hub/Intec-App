import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64

# 1. IMPOSTAZIONE GRAFICA E LOGO
st.set_page_config(page_title="INTEC - Calcolatore ROI", layout="wide")

# Funzione per convertire le immagini per lo scambio dinamico
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return None

# Carichiamo entrambi i loghi
logo_positive = get_image_base64("INTEC-logo-V1-2colori-POSITIVE.png")
logo_negative = get_image_base64("INTEC-logo-V1-2colori-NEGATIVE.png")

if logo_positive and logo_negative:
    # CSS: Logo centrato e scambio dinamico Light/Dark
    st.markdown(f"""
        <style>
            .logo-outer-container {{
                display: flex;
                justify-content: center;
                width: 100%;
                margin-bottom: 30px;
            }}
            .logo-container {{
                width: 450px;
            }}
            .logo-light {{ display: block; width: 100%; }}
            .logo-dark {{ display: none; width: 100%; }}
            
            @media (prefers-color-scheme: dark) {{
                .logo-light {{ display: none; }}
                .logo-dark {{ display: block; }}
            }}
        </style>
        <div class="logo-outer-container">
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_positive}" class="logo-light">
                <img src="data:image/png;base64,{logo_negative}" class="logo-dark">
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.title("🟢 INTEC SYSTEMS")

st.markdown("<h3 style='text-align: center;'>Calcolatore di Efficienza e ROI — Supporto alla Vendita</h3>", unsafe_allow_html=True)
st.markdown("---")

# 2. CARICAMENTO DATABASE EXCEL (Invariato)
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
st.markdown("#### 2. Analisi Comparativa e Configurazione Tecnica")
col_intec, col_cliente = st.columns(2)

# --- COLONNA SINISTRA: SISTEMA INTEC (AVANZATO) ---
with col_intec:
    st.subheader("🟢 Sistema INTEC")
    
    # Nuove specifiche tecniche richieste
    tipo_rinforzo = st.selectbox("Tipo di Rinforzo (MAT/OZ):", ["MAT 300", "MAT 450", "OZ 1", "OZ 1.5"])
    
    # Calcolo PF07E
    kg_pf07e = superficie * 14.0
    peso_fusto = 140.0 # Ipotizzato 25kg per fusto
    fusti_pf07e = kg_pf07e / peso_fusto
    
    # Calcolo R999
    kg_r999 = superficie * 0.468
    
    kg_tot_intec = kg_pf07e + kg_r999
    
    # Visualizzazione dati tecnici nel pannello
    st.markdown(f"""
    **Configurazione Materiali:**
    - 📦 **PF07E:** {kg_pf07e:.1f} kg (circa **{fusti_pf07e:.1f} fusti** da 25kg)
    - 🧪 **Resina R999:** {kg_r999:.2f} kg per laminazione
    - 🏗️ **Rinforzo:** {tipo_rinforzo}
    """)
    
    prezzo_intec_base = 10.70
    prezzo_intec_input = st.number_input("Prezzo Materiale INTEC (Medio €/KG):", min_value=0.0, value=prezzo_intec_base, step=0.1)
    
    # Ore manodopera (Logica semplificata come prima, poi la collegheremo al DB)
    ore_intec = (superficie / 5.0) + 2.0
    st.warning(f"⏱️ Ore Manodopera Stimate: {ore_intec:.1f} h")
    
    costo_orario_intec = st.number_input("Costo Orario Manodopera (€/h):", min_value=0.0, value=25.0, step=1.0)
    
    tot_mat_intec = kg_tot_intec * prezzo_intec_input
    tot_mano_intec = ore_intec * costo_orario_intec
    tot_generale_intec = tot_mat_intec + tot_mano_intec

# --- COLONNA DESTRA: METODO CLIENTE (Invariato) ---
with col_cliente:
    st.subheader("⚪ Metodo Attuale Cliente")
    tecnologia = st.selectbox("Tecnologia Concorrente:", ["Epossidica", "Spray", "Laminazione Manuale"])
    
    kg_cliente = st.number_input(f"Totale materiale Cliente (KG):", min_value=0.0, value=0.0, step=10.0)
    prezzo_cliente = st.number_input(f"Prezzo al KG Cliente:", min_value=0.0, value=0.0, step=0.5)
    
    ore_cliente = st.number_input(f"Ore totali cantiere Cliente:", min_value=0.0, value=0.0, step=1.0)
    costo_orario_cliente = st.number_input(f"Costo orario Cliente:", min_value=0.0, value=0.0, step=1.0)
    
    tot_mat_cliente = kg_cliente * prezzo_cliente
    tot_mano_cliente = ore_cliente * costo_orario_cliente
    tot_generale_cliente = tot_mat_cliente + tot_mano_cliente

st.markdown("---")

# 5. DUE GRAFICI SEPARATI E AFFIANCATI (TEMA AUTOMATICO)
st.markdown("#### 3. Analisi Visiva d'Impatto")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    fig_costi = go.Figure()
    fig_costi.add_trace(go.Bar(
        x=['Sistema INTEC', 'Metodo Cliente'],
        y=[tot_generale_intec, tot_generale_cliente],
        marker_color=['#008F99', '#4A4A4A'],
        text=[f"{tot_generale_intec:,.2f} {valuta}", f"{tot_generale_cliente:,.2f} {valuta}"],
        textposition='auto',
        textfont=dict(color='white')
    ))
    fig_costi.update_layout(
        title=dict(text="Confronto Costo Totale", font=dict(size=16)),
        yaxis=dict(title="Spesa Totale", showgrid=True)
    )
    st.plotly_chart(fig_costi, use_container_width=True, theme="streamlit")

with col_chart2:
    fig_ore = go.Figure()
    fig_ore.add_trace(go.Bar(
        x=['Sistema INTEC', 'Metodo Cliente'],
        y=[ore_intec, ore_cliente],
        marker_color=['#008F99', '#4A4A4A'],
        text=[f"{ore_intec:.1f} h", f"{ore_cliente:.1f} h"],
        textposition='auto',
        textfont=dict(color='white') 
    ))
    fig_ore.update_layout(
        title=dict(text="Confronto Tempistiche", font=dict(size=16)),
        yaxis=dict(title="Ore Totali (h)", showgrid=True)
    )
    st.plotly_chart(fig_ore, use_container_width=True, theme="streamlit")

# 6. BANNER DI CHIUSURA ROI
st.markdown("---")
risparmio_economico = tot_generale_cliente - tot_generale_intec
ore_risparmiate = ore_cliente - ore_intec

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label="COSTO TOTALE SISTEMA INTEC", value=f"{tot_generale_intec:,.2f} {valuta}")
with col_res2:
    st.metric(label="COSTO TOTALE METODO CLIENTE", value=f"{tot_generale_cliente:,.2f} {valuta}")

if tot_generale_cliente > 0:
    st.success(f"💰 **Risparmio Economico Netto:** {risparmio_economico:,.2f} {valuta} | ⏱️ **Tempo Guadagnato:** {ore_risparmiate:.1f} ore")

st.markdown("---")
st.caption("⚠️ **Nota Tecnica:** I tempi di indurimento e fresabilità variano in base alla temperatura e alla catalisi.")
