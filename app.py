import streamlit as st
import plotly.graph_objects as go
import base64
import datetime

# 1. IMPOSTAZIONE GRAFICA E LOGO
st.set_page_config(page_title="Intec App", layout="wide")

# Funzione Logo
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return None

# 2. CONFIGURAZIONE PROGETTO
st.markdown("<h3 style='text-align: center;'>Calcolatore di Efficienza e ROI</h3>", unsafe_allow_html=True)
col_c1, col_c2, col_c3 = st.columns(3)
with col_c1: superficie = st.number_input("Superficie:", min_value=0.0, value=10.0, step=1.0)
with col_c2: unita = st.selectbox("Unità:", ["Metri Quadri (m²)", "Piedi Quadri (sq ft)"])
with col_c3: valuta = st.selectbox("Valuta:", ["Euro (€)", "Dollaro ($)"])

# Logica Conversione
superficie_m2 = superficie if unita == "Metri Quadri (m²)" else superficie / 10.7639
is_sqft = (unita == "Piedi Quadri (sq ft)")
valuta_simbolo = "$" if valuta == "Dollaro ($)" else "€"
unita_peso_str = "lbs" if is_sqft else "kg"

st.markdown("---")

# ==========================================
# FASE 1: LAMINAZIONE
# ==========================================
st.markdown("#### 2. Fase 1: Laminazione Resina")
col_int, col_cli = st.columns(2)

with col_int:
    st.markdown("##### 🟢 INTEC (R999)")
    st.markdown("🛠️ **Tecnologia:** R999 Intec | ⚖️ **Rapporto:** 1:2,5")
    metodo = st.selectbox("Metodo Applicazione:", ["Applicazione manuale", "Applicazione con taglio e spruzzo"], key="m1")
    is_spray = (metodo == "Applicazione con taglio e spruzzo")
    rinf = st.selectbox("Tipo Rinforzo:", ["MAT 300", "MAT 450", "OZ 1.0", "OZ 1.5"], disabled=is_spray, key="r1")
    prz = st.number_input(f"Prezzo R999 ({valuta_simbolo}/{unita_peso_str}):", value=5.0, step=0.1, key="p1")
    ore = st.number_input("Ore Manodopera:", value=float(superficie_m2 * (2.0/60.0 if is_spray else 20.0/60.0)), step=0.1, key="o1")
    tar = st.number_input(f"Tariffa ({valuta_simbolo}/h):", value=35.0, step=1.0, key="t1")
    
    # Calcolo
    kg = superficie_m2 * (1.5 if rinf=="MAT 300" else 2.25 if rinf=="MAT 450" else 0.312 if rinf=="OZ 1.0" else 0.468)
    tot_mat = (kg * 2.20462 if is_sqft else kg) * prz
    tot_mano = ore * tar
    tot_intec1 = tot_mat + tot_mano
    st.info(f"**Specifiche:**\n- 🧶 Rinforzo: {'N/D' if is_spray else rinf}\n- 🧪 Resa: {kg:.2f} {unita_peso_str}\n- ⏱️ Manodopera: {ore}h *(1 persona)*")
    st.success(f"**Subtotale:** {tot_intec1:,.2f} {valuta_simbolo}")

with col_cli:
    st.markdown("##### ⚪ CLIENTE (Resina)")
    tec_cli = st.selectbox("Tecnologia:", ["Epossidica", "Duratec"], key="tc1")
    metodo_cli = st.selectbox("Metodo:", ["Applicazione manuale", "Applicazione con taglio e spruzzo"], key="mc1")
    rinf_cli = st.selectbox("Rinforzo:", ["MAT 300", "MAT 450", "OZ 1.0", "OZ 1.5"], disabled=(metodo_cli == "Applicazione con taglio e spruzzo"), key="rc1")
    qta_cli = st.number_input(f"Quantità ({unita_peso_str}):", value=0.0, step=1.0, key="q1")
    prz_cli = st.number_input(f"Prezzo ({valuta_simbolo}/{unita_peso_str}):", value=0.0, step=0.1, key="pc1")
    ore_cli = st.number_input("Ore Lavoro:", value=0.0, step=0.5, key="oc1")
    tar_cli = st.number_input(f"Tariffa ({valuta_simbolo}/h):", value=35.0, step=1.0, key="tc1_t")
    
    tot_cli1 = (qta_cli * prz_cli) + (ore_cli * tar_cli)
    st.info(f"**Specifiche:**\n- 🧶 Rinforzo: {rinf_cli}\n- 🧪 Materiale: {qta_cli} {unita_peso_str}\n- ⏱️ Manodopera: {ore_cli}h *(1 persona)*")
    st.info(f"**Subtotale:** {tot_cli1:,.2f} {valuta_simbolo}")

# ==========================================
# FASE 2: PASTE
# ==========================================
st.markdown("---")
st.markdown("#### 3. Fase 2: Applicazione Paste")
col_p1, col_p2 = st.columns(2)

with col_p1:
    prod = st.selectbox("Prodotto Base:", ["PF07E", "PF07LS", "PF10E", "PF10GT", "PV10E"])
    prz_p = st.number_input(f"Prezzo {prod} ({valuta_simbolo}/{unita_peso_str}):", value=10.70, step=0.1)
    ore_p = st.number_input("Ore Manodopera:", value=round(superficie_m2 / 5.0, 2), step=0.5)
    tar_p = st.number_input(f"Tariffa ({valuta_simbolo}/h):", value=35.0, step=1.0)
    # Calcolo
    kg_p = superficie_m2 * (20.0 * (0.7 if "07" in prod else 1.0))
    tot_intec2 = ((kg_p * 2.20462 if is_sqft else kg_p) * prz_p) + (ore_p * tar_p)
    st.info(f"**Specifiche Paste:**\n- 📦 Prodotto: {prod}\n- ⏱️ Manodopera: {ore_p}h *(1 persona)*")
    st.success(f"**Subtotale:** {tot_intec2:,.2f} {valuta_simbolo}")

with col_p2:
    tec_p_cli = st.selectbox("Tecnologia Paste:", ["Epossidica", "Spraycore"], key="tpc2")
    qta_p_cli = st.number_input(f"Quantità Paste ({unita_peso_str}):", value=0.0, step=1.0)
    prz_p_cli = st.number_input(f"Prezzo Paste ({valuta_simbolo}/{unita_peso_str}):", value=0.0, step=0.1)
    ore_p_cli = st.number_input("Ore Paste:", value=0.0, step=0.5)
    tar_p_cli = st.number_input(f"Tariffa Paste ({valuta_simbolo}/h):", value=35.0, step=1.0)
    
    tot_cli2 = (qta_p_cli * prz_p_cli) + (ore_p_cli * tar_p_cli)
    st.info(f"**Specifiche Paste:**\n- 📦 Tecnologia: {tec_p_cli}\n- 🧪 Materiale: {qta_p_cli} {unita_peso_str}\n- ⏱️ Manodopera: {ore_p_cli}h *(1 persona)*")
    st.info(f"**Subtotale:** {tot_cli2:,.2f} {valuta_simbolo}")

# Riepilogo Finale
st.markdown("---")
st.markdown("#### 4. Riepilogo Finale")
col_r1, col_r2 = st.columns(2)
with col_r1: st.metric("TOTALE INTEC", f"{(tot_intec1 + tot_intec2):,.2f} {valuta_simbolo}")
with col_r2: st.metric("TOTALE CLIENTE", f"{(tot_cli1 + tot_cli2):,.2f} {valuta_simbolo}")
