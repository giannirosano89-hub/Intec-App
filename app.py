import streamlit as st
import plotly.graph_objects as go
import base64
import datetime

# ─────────────────────────────────────────────
# COSTANTI CENTRALIZZATE
# ─────────────────────────────────────────────

MOLTIPLICATORI_R999 = {
    "MAT 300": 1.5,
    "MAT 450": 2.25,
    "OZ 1.0":  0.312,
    "OZ 1.5":  0.468,
}

SOGLIA_FUSTO_KG   = 175.0
PESO_LATTA_KG     = 25.0
PESO_FUSTO_KG     = 225.0
PESO_FUSTO_GAL    = 55.0
SPESSORE_MM       = 16
M2_PER_ORA        = 5.0
ORE_SETUP         = 2.0
CONSUMO_BASE_M2   = 20.0   # kg/m² per prodotti PF a peso specifico 1.0
PESO_FUSTO_BASE   = 200.0  # kg per prodotti a peso specifico 1.0

PRODOTTI = ["PF07E", "PF07LS", "PF10E", "PF10GT", "PV10E"]
RINFORZI = ["MAT 300", "MAT 450", "OZ 1.0", "OZ 1.5"]

SQ_FT_PER_M2  = 10.7639
LBS_PER_KG    = 2.20462
INCH_PER_MM   = 1 / 25.4


# ─────────────────────────────────────────────
# HELPER: IMMAGINI
# ─────────────────────────────────────────────

def get_image_base64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


# ─────────────────────────────────────────────
# HELPER: CONVERSIONI
# ─────────────────────────────────────────────

def to_m2(valore: float, unita: str) -> float:
    return valore if unita == "Metri Quadri (m²)" else valore / SQ_FT_PER_M2


def to_display_peso(kg: float, us: bool) -> float:
    return kg * LBS_PER_KG if us else kg


# ─────────────────────────────────────────────
# CALCOLI INTEC
# ─────────────────────────────────────────────

def calcola_prodotto_intec(prodotto: str, superficie_m2: float) -> dict:
    """Calcola kg e fusti del prodotto base INTEC."""
    peso_specifico = 0.7 if "07" in prodotto else 1.0
    consumo_m2     = CONSUMO_BASE_M2 * peso_specifico
    peso_fusto     = PESO_FUSTO_BASE * peso_specifico
    kg             = superficie_m2 * consumo_m2
    fusti          = kg / peso_fusto
    return {"kg": kg, "fusti": fusti, "peso_fusto": peso_fusto}


def calcola_r999(rinforzo: str, superficie_m2: float, superficie_sqft: float) -> float:
    """Calcola kg di resina R999 sempre in KG (unità interna)."""
    mol = MOLTIPLICATORI_R999[rinforzo]
    if "MAT" in rinforzo:
        return superficie_m2 * mol
    else:
        # OZ: moltiplicatore è oz/sqft → converti in kg
        oz_totali = superficie_sqft * mol
        return oz_totali / (LBS_PER_KG * 16)   # 16 oz = 1 lb


def calcola_ore_intec(superficie_m2: float) -> float:
    return (superficie_m2 / M2_PER_ORA) + ORE_SETUP


def calcola_costo_intec(kg_prodotto: float, kg_r999: float,
                        prezzo_prodotto: float, prezzo_resina: float,
                        us: bool) -> float:
    mult = LBS_PER_KG if us else 1.0
    return (kg_prodotto * mult * prezzo_prodotto) + (kg_r999 * mult * prezzo_resina)


# ─────────────────────────────────────────────
# FORMATTAZIONE TESTI MATERIALI
# ─────────────────────────────────────────────

def testo_prodotto(risultato: dict, us: bool, valuta: str) -> str:
    fusti  = risultato["fusti"]
    peso_f = risultato["peso_fusto"]
    sp     = SPESSORE_MM * INCH_PER_MM
    if us:
        galloni = fusti * PESO_FUSTO_GAL
        return (f"{galloni:.1f} gallons ({fusti:.1f} drums × {PESO_FUSTO_GAL:.0f} gal) "
                f"— *thickness {sp:.2f} inch*")
    return f"{fusti:.1f} fusti (da {peso_f:.0f} kg) — *spessore {SPESSORE_MM}mm*"


def testo_r999(kg: float, us: bool) -> str:
    display = to_display_peso(kg, us)
    unita   = "lbs" if us else "kg"
    nota    = "laminazione 2 strati"

    if kg < SOGLIA_FUSTO_KG:
        latte = kg / PESO_LATTA_KG
        ct    = f"{latte:.1f} {'pails' if us else 'latte'} (25 kg)"
    else:
        fusti = kg / PESO_FUSTO_KG
        if us:
            ct = f"{fusti * PESO_FUSTO_GAL:.1f} gallons / {fusti:.1f} drums (55 gal)"
        else:
            ct = f"{fusti:.1f} fusti (da {PESO_FUSTO_KG:.0f} kg)"

    return f"{display:.2f} {unita} [{ct}] — *{nota}*"


# ─────────────────────────────────────────────
# STAMPA: testo fantasma unificato
# ─────────────────────────────────────────────

def print_row(html: str):
    st.markdown(f"<div class='print-text'>{html}</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────

def main():
    # --- PAGE CONFIG ---
    st.set_page_config(
        page_title="Intec App",
        page_icon="INTEC-logo-V1-2colori-NEGATIVE.png",
        layout="wide",
    )

    logo_pos = get_image_base64("INTEC-logo-V1-2colori-POSITIVE.png")
    logo_neg = get_image_base64("INTEC-logo-V1-2colori-NEGATIVE.png")

    st.markdown(f"""
    <style>
        .block-container {{ padding-top: 2rem !important; padding-bottom: 0.5rem !important; }}
        .logo-outer {{ display: flex; justify-content: center; width: 100%; margin-bottom: -10px; }}
        .logo-wrap  {{ width: 320px; max-width: 100%; }}
        .logo-light {{ display: block; width: 100%; }}
        .logo-dark  {{ display: none;  width: 100%; }}
        .print-text {{ display: none; }}

        @media (prefers-color-scheme: dark) {{
            .logo-light {{ display: none; }}
            .logo-dark  {{ display: block; }}
        }}

        @media (max-width: 768px) {{
            .logo-wrap {{ width: 200px; }}
        }}

        @media print {{
            @page {{ margin: 0.5cm; size: A4 portrait; }}

            .stButton, .stNumberInput, .stSelectbox,
            .stDateInput, .stTextInput,
            header[data-testid="stHeader"],
            [data-testid="stSidebar"], footer, #MainMenu {{
                display: none !important;
            }}

            .print-text {{
                display: block !important;
                font-size: 13px !important;
                margin: 5px 0 8px !important;
                line-height: 1.4 !important;
                color: black !important;
            }}

            .main, .block-container {{
                background: white !important;
                color: black !important;
                padding: 0 !important;
                margin: 0 !important;
            }}

            .logo-dark  {{ display: none !important; }}
            .logo-light {{ display: block !important; width: 220px !important; margin: 0 auto 10px !important; }}

            div[data-testid="column"] {{
                width: 48% !important; flex: 1 1 48% !important;
                min-width: 48% !important; display: inline-block !important;
                vertical-align: top;
            }}

            div[data-testid="stAlert"] {{
                background: white !important; color: black !important;
                border: 2px solid #008F99 !important;
                padding: 10px !important; margin: 5px 0 !important;
            }}
            div[data-testid="stAlert"] * {{ color: black !important; }}

            h3 {{ font-size: 16px !important; margin: 5px 0 !important; }}
            h4 {{ font-size: 14px !important; margin: 8px 0 5px !important; }}
            p, ul, li {{ font-size: 12px !important; margin: 3px 0 !important; padding: 0 !important; }}
            hr {{ margin: 8px 0 !important; border-top: 1px solid #ccc !important; }}
            .js-plotly-plot .plotly text {{ fill: #000 !important; font-size: 12px !important; }}
        }}
    </style>
    <div class="logo-outer">
        <div class="logo-wrap">
            <img src="data:image/png;base64,{logo_pos}" class="logo-light">
            <img src="data:image/png;base64,{logo_neg}" class="logo-dark">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── INTESTAZIONE ──────────────────────────────────────────────────
    st.markdown("<h3 style='text-align:center; margin-top:0;'>Calcolatore di Efficienza e ROI</h3>",
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        nome_commerciale = st.text_input("💼 Nome Commerciale INTEC:", placeholder="Es. Mario Rossi")
    with c2:
        nome_cliente = st.text_input("👤 Nome Cliente / Cantiere:", placeholder="Es. Cantiere Navale")
    with c3:
        data_offerta = st.date_input("📅 Data Offerta:", value=datetime.date.today(), format="DD/MM/YYYY")

    comm = nome_commerciale or "Non specificato"
    cli  = nome_cliente     or "Non specificato"
    print_row(
        f"<b>💼 Commerciale:</b> {comm} &nbsp;|&nbsp; "
        f"<b>👤 Cliente:</b> {cli} &nbsp;|&nbsp; "
        f"<b>📅 Data:</b> {data_offerta.strftime('%d/%m/%Y')}"
    )
    st.markdown("---")

    # ── CONFIGURAZIONE PROGETTO ───────────────────────────────────────
    st.markdown("#### 1. Configurazione Progetto")
    c1, c2, c3 = st.columns(3)
    with c1:
        superficie = st.number_input("Superficie da trattare:", min_value=0.0, value=10.0, step=1.0)
    with c2:
        unita = st.selectbox("Unità di Misura:", ["Metri Quadri (m²)", "Piedi Quadri (sq ft)"])
    with c3:
        valuta = st.selectbox("Valuta:", ["Euro (€)", "Dollaro ($)"])

    us = (unita == "Piedi Quadri (sq ft)") and (valuta == "Dollaro ($)")
    v_sim   = "$" if us else "€"
    u_peso  = "lbs" if us else "kg"

    superficie_m2   = to_m2(superficie, unita)
    superficie_sqft = superficie_m2 * SQ_FT_PER_M2

    print_row(f"<b>Superficie:</b> {superficie} {unita} &nbsp;|&nbsp; <b>Valuta:</b> {valuta}")
    st.markdown("---")

    # ── ANALISI COMPARATIVA ───────────────────────────────────────────
    st.markdown("#### 2. Analisi Comparativa Applicazione e Tempi")
    col_intec, col_cli = st.columns(2)

    # ── COLONNA INTEC ─────────────────────────────────────────────────
    with col_intec:
        st.markdown(
            "<h3 style='margin-bottom:0'>"
            "<span style='display:inline-block;width:15px;height:15px;"
            "background:#008F99;border-radius:50%;vertical-align:middle;margin-right:5px'></span>"
            "Sistema INTEC</h3>",
            unsafe_allow_html=True,
        )

        cs1, cs2 = st.columns(2)
        with cs1:
            prodotto = st.selectbox("Prodotto:", PRODOTTI)
        with cs2:
            rinforzo = st.selectbox("Tipo di Rinforzo:", RINFORZI)

        # calcoli
        ris_prod = calcola_prodotto_intec(prodotto, superficie_m2)
        kg_r999  = calcola_r999(rinforzo, superficie_m2, superficie_sqft)
        ore_intec = calcola_ore_intec(superficie_m2)

        st.markdown(f"""
**Specifiche Tecniche:**
- 📦 **{prodotto}:** {testo_prodotto(ris_prod, us, valuta)}
- 🧪 **Resina R999 ({rinforzo}):** {testo_r999(kg_r999, us)}
""")

        cp1, cp2 = st.columns(2)
        with cp1:
            lbl_p = f"Prezzo {prodotto} ($/{u_peso}):" if us else f"Prezzo {prodotto} (€/kg):"
            prezzo_prodotto = st.number_input(lbl_p, min_value=0.0, value=10.70, step=0.1)
        with cp2:
            lbl_r = f"Costo Resina R999 ($/{u_peso}):" if us else "Costo Resina R999 (€/kg):"
            prezzo_resina = st.number_input(lbl_r, min_value=0.0, value=5.00, step=0.1)

        print_row(
            f"<b>Prezzi INTEC:</b> {prodotto}: {prezzo_prodotto:.2f} {v_sim}/{u_peso} &nbsp;|&nbsp; "
            f"Resina R999: {prezzo_resina:.2f} {v_sim}/{u_peso}"
        )

        st.success(f"⏱️ Ore Manodopera Stimate: {ore_intec:.1f} h")

        tot_intec = calcola_costo_intec(
            ris_prod["kg"], kg_r999, prezzo_prodotto, prezzo_resina, us
        )

    # ── COLONNA CLIENTE ───────────────────────────────────────────────
    with col_cli:
        st.markdown(
            "<h3 style='margin-bottom:0'>"
            "<span style='display:inline-block;width:15px;height:15px;"
            "background:#4A4A4A;border-radius:50%;vertical-align:middle;margin-right:5px'></span>"
            "Metodo Attuale Cliente</h3>",
            unsafe_allow_html=True,
        )

        tecnologia = st.selectbox("Tecnologia Corrente:", ["Epossidica", "Spray"])

        cq1, cq2 = st.columns(2)
        with cq1:
            lbl_mq = f"Quantità Materiale ({u_peso}):" if us else f"Quantità Materiale (kg):"
            kg_cliente = st.number_input(lbl_mq, min_value=0.0, value=0.0, step=10.0)
        with cq2:
            lbl_rq = f"Quantità Resina ({u_peso}):" if us else "Quantità Resina (kg):"
            kg_resina_cli = st.number_input(lbl_rq, min_value=0.0, value=0.0, step=10.0)

        cp1, cp2 = st.columns(2)
        with cp1:
            lbl_pm = f"Prezzo Mat. ($/{u_peso}):" if us else "Prezzo Mat. (€/kg):"
            prezzo_cli = st.number_input(lbl_pm, min_value=0.0, value=0.0, step=0.5)
        with cp2:
            lbl_pr = f"Prezzo Resina ($/{u_peso}):" if us else "Prezzo Resina (€/kg):"
            prezzo_resina_cli = st.number_input(lbl_pr, min_value=0.0, value=0.0, step=0.5)

        ore_cliente = st.number_input("Ore totali cantiere Cliente:", min_value=0.0, value=0.0, step=1.0)

        print_row(
            f"<b>Tecnologia:</b> {tecnologia} &nbsp;|&nbsp; "
            f"Materiale: {kg_cliente:.1f} {u_peso} a {prezzo_cli:.2f} {v_sim}/{u_peso} &nbsp;|&nbsp; "
            f"Resina: {kg_resina_cli:.1f} {u_peso} a {prezzo_resina_cli:.2f} {v_sim}/{u_peso} &nbsp;|&nbsp; "
            f"Ore: {ore_cliente:.1f} h"
        )

        tot_cliente = (kg_cliente * prezzo_cli) + (kg_resina_cli * prezzo_resina_cli)

        # Validazione: avviso se tutti i dati cliente sono a zero
        if kg_cliente == 0 and kg_resina_cli == 0 and ore_cliente == 0:
            st.warning("⚠️ Inserisci i dati del metodo cliente per abilitare il confronto.")

    st.markdown("---")

    # ── GRAFICI RESPONSIVE ────────────────────────────────────────────
    st.markdown("#### 3. Impatto Visivo Risultati")

    def bar_chart(titolo, valori, etichette):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Sistema INTEC", "Metodo Cliente"],
            y=valori,
            marker_color=["#008F99", "#4A4A4A"],
            text=etichette,
            textposition="auto",
            textfont=dict(color="white"),
            width=0.35,
        ))
        fig.update_layout(
            height=240,
            title=dict(text=titolo, font=dict(size=13)),
            yaxis=dict(showgrid=True),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=35, b=20),
        )
        return fig

    cg1, cg2 = st.columns(2)
    with cg1:
        st.plotly_chart(
            bar_chart(
                "Costo Materiali",
                [tot_intec, tot_cliente],
                [f"{tot_intec:,.2f} {v_sim}", f"{tot_cliente:,.2f} {v_sim}"],
            ),
            use_container_width=True,
            config={"staticPlot": True},
        )
    with cg2:
        st.plotly_chart(
            bar_chart(
                "Ore di Lavoro",
                [ore_intec, ore_cliente],
                [f"{ore_intec:.1f} h", f"{ore_cliente:.1f} h"],
            ),
            use_container_width=True,
            config={"staticPlot": True},
        )

    # ── BANNER FINALE ─────────────────────────────────────────────────
    st.markdown("---")
    risparmio  = tot_cliente - tot_intec
    ore_guad   = ore_cliente - ore_intec

    r1, r2 = st.columns(2)
    with r1:
        st.metric("TOTALE MATERIALI INTEC (IVA incl.)",  f"{tot_intec:,.2f} {v_sim}")
    with r2:
        st.metric("TOTALE MATERIALI CLIENTE (IVA incl.)", f"{tot_cliente:,.2f} {v_sim}")

    if tot_cliente > 0:
        st.success(
            f"💰 **Risparmio Netto sui Materiali:** {risparmio:,.2f} {v_sim} "
            f"| ⏱️ **Tempo Guadagnato:** {ore_guad:.1f} ore"
        )

    st.markdown("---")
    st.markdown(
        "<p style='font-size:11px; font-style:italic; margin-top:0'>"
        "⚠️ <b>Nota Tecnica:</b> I tempi di indurimento e fresabilità variano "
        "in base alla temperatura e alla catalisi.</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
