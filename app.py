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
    
    kg_cliente = st.number_input(f"Quantità materiale totale usata dal Cliente (KG):", min_value=0.0, value=0.0, step=10.0)
    prezzo_cliente = st.number_input(f"Prezzo al KG pagato dal Cliente:", min_value=0.0, value=0.0, step=0.5)
    
    ore_cliente = st.number_input(f"Ore totali impiegate nel cantiere dal Cliente:", min_value=0.0, value=0.0, step=1.0)
    costo_orario_cliente = st.number_input(f"Costo orario della manodopera Cliente:", min_value=0.0, value=0.0, step=1.0)
    
    tot_mat_cliente = kg_cliente * prezzo_cliente
    tot_mano_cliente = ore_cliente * costo_orario_cliente
    tot_generale_cliente = tot_mat_cliente + tot_mano_cliente

st.markdown("---")

# 5. DUE GRAFICI SEPARATI E AFFIANCATI
st.markdown("#### 3. Analisi Visiva d'Impatto")

# Creiamo due colonne per affiancare i grafici
col_chart1, col_chart2 = st.columns(2)

# --- GRAFICO 1: CONFRONTO COSTI (Colonna Sinistra) ---
with col_chart1:
    fig_costi = go.Figure()
    fig_costi.add_trace(go.Bar(
        x=['Sistema INTEC', 'Metodo Cliente'],
        y=[tot_generale_intec, tot_generale_cliente],
        marker_color=['#008F99', '#4A4A4A'], # Verde INTEC vs Grigio Cliente
        text=[f"{tot_generale_intec:,.2f} {valuta}", f"{tot_generale_cliente:,.2f} {valuta}"],
        textposition='auto',
    ))
    fig_costi.update_layout(
        template='plotly_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=dict(text=f"Confronto Costo Totale ({valuta})", font=dict(color='#4A4A4A', size=16)),
        xaxis=dict(tickfont=dict(color='#4A4A4A', size=12)),
        yaxis=dict(title=f"Spesa Totale", titlefont=dict(color='#4A4A4A'), tickfont=dict(color='#4A4A4A'), showgrid=True)
    )
    st.plotly_chart(fig_costi, use_container_width=True)

# --- GRAFICO 2: CONFRONTO ORE (Colonna Destra) ---
with col_chart2:
    fig_ore = go.Figure()
    fig_ore.add_trace(go.Bar(
        x=['Sistema INTEC', 'Metodo Cliente'],
        y=[ore_intec, ore_cliente],
        marker_color=['#00BAC7', '#A6A6A6'], # Variante chiara INTEC vs Grigio chiaro Cliente
        text=[f"{ore_intec:.1f} h", f"{ore_cliente:.1f} h"],
        textposition='auto',
    ))
    fig_ore.update_layout(
        template='plotly_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=dict(text="Confronto Tempistiche (Ore di Lavoro)", font=dict(color='#4A4A4A', size=16)),
        xaxis=dict(tickfont=dict(color='#4A4A4A', size=12)),
        yaxis=dict(title="Ore Totali (h)", titlefont=dict(color='#4A4A4A'), tickfont=dict(color='#4A4A4A'), showgrid=True)
    )
    st.plotly_chart(fig_ore, use_container_width=True)

# 6. BANNER DI CHIUSURA COMMERCIALE (ROI)
st.markdown("---")
risparmio_economico = tot_generale_cliente - tot_generale_intec
ore_risparmiate = ore_cliente - ore_intec

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label="COSTO TOTALE SISTEMA INTEC", value=f"{tot_generale_intec:,.2f} {valuta}")
with col_res2:
    st.metric(label="COSTO TOTALE METODO CLIENTE", value=f"{tot_generale_cliente:,.2f} {valuta}")

if tot_generale_cliente > 0:
    st.success(f"💰 **Risparmio Economico Netto per il Cliente:** {risparmio_economico:,.2f} {valuta} | ⏱️ **Tempo Guadagnato:** {ore_risparmiate:.1f} ore di lavoro in meno!")

# 7. NOTA TECNICA IN CALCE
st.markdown("---")
st.caption("⚠️ **Nota Tecnica di Processo:** La pasta INTEC è fresabile dopo circa **12 ore**. I tempi possono subire variazioni in base alla temperatura dell'ambiente di lavoro e alla percentuale di catalisi utilizzata.")
