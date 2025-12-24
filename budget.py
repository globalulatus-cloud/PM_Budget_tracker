import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

st.set_page_config(
    page_title="Project Budget Tracker",
    layout="wide",
)

# -------------------------------------------------
# Constants
# -------------------------------------------------
CURRENCIES = ["JPY", "USD", "KRW", "EUR"]

COST_TYPES = [
    "Translator fees",
    "Checker fees",
    "MTPE fees",
    "FR fees",
    "Formatting fees",
    "LSO fees",
    "LQA fees",
]

CALC_METHODS = [
    "Per word",
    "Per minute",
    "Per hour",
    "Per page",
    "Per character",
    "Flat fee",
]

ROUNDING_RULES = {"JPY": 0, "KRW": 0, "USD": 2, "EUR": 2}

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def calculate_cost(rate, volume, method):
    if not rate:
        return 0.0
    if method == "Flat fee":
        return rate
    return rate * volume if volume else 0.0

def round_currency(value, currency):
    return round(float(value), ROUNDING_RULES.get(currency, 2))

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "cost_rows" not in st.session_state:
    st.session_state.cost_rows = []

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("💰 Project Budget Tracker")
st.caption("Track internal costs against the approved client budget")

# =================================================
# CLIENT BUDGET CARD
# =================================================
with st.container(border=True):
    st.subheader("📌 Client Approved Budget")

    c1, c2 = st.columns([1, 2])
    with c1:
        client_currency = st.selectbox("Currency", CURRENCIES)
    with c2:
        client_budget = st.number_input(
            "Approved Budget Amount",
            min_value=0.0,
            step=1000.0,
            format="%.2f",
        )

# =================================================
# ADD COST FORM
# =================================================
with st.container(border=True):
    st.subheader("➕ Add Internal Cost")

    with st.form("cost_form", clear_on_submit=True):
        r1 = st.columns(3)
        r2 = st.columns(3)
        r3 = st.columns(3)

        cost_type = r1[0].selectbox("Cost Type", COST_TYPES)
        calc_method = r1[1].selectbox("Calculation Method", CALC_METHODS)
        currency = r1[2].selectbox("Currency", CURRENCIES)

        volume = r2[0].number_input("Volume", min_value=0.0, format="%.4f")
        rate = r2[1].number_input("Rate", min_value=0.0, format="%.4f")
        vendor = r2[2].text_input("Vendor")

        submit = r3[0].form_submit_button("Add Cost")

        if submit:
            cost = calculate_cost(rate, volume, calc_method)
            st.session_state.cost_rows.append({
                "Cost Type": cost_type,
                "Vendor": vendor,
                "Method": calc_method,
                "Volume": volume,
                "Rate": rate,
                "Currency": currency,
                "Internal Cost": cost,
            })
            st.success("Cost added successfully")

# =================================================
# COST LIST
# =================================================
if st.session_state.cost_rows:
    with st.container(border=True):
        st.subheader("📄 Internal Cost Breakdown")

        for idx, row in enumerate(st.session_state.cost_rows):
            with st.container(border=True):
                c = st.columns([2, 2, 2, 1.5, 1.5, 1.5, 1])

                c[0].markdown(f"**{row['Cost Type']}**")
                c[1].write(row["Vendor"] or "—")
                c[2].write(row["Method"])
                c[3].write(row["Volume"])
                c[4].write(row["Rate"])
                c[5].markdown(
                    f"**{round_currency(row['Internal Cost'], row['Currency'])}**"
                )
                c[6].write(row["Currency"])

                if c[6].button("🗑️", key=f"delete_{idx}"):
                    st.session_state.cost_rows.pop(idx)
                    st.rerun()

    # =================================================
    # BUDGET HEALTH
    # =================================================
    total_internal = sum(r["Internal Cost"] for r in st.session_state.cost_rows)
    utilization = (total_internal / client_budget * 100) if client_budget else 0

    with st.container(border=True):
        st.subheader("📊 Budget Health")

        m1, m2, m3 = st.columns(3)
        m1.metric("Client Budget", f"{round_currency(client_budget, client_currency)} {client_currency}")
        m2.metric("Total Internal Cost", f"{round_currency(total_internal, client_currency)} {client_currency}")
        m3.metric("Utilization %", f"{round(utilization, 2)} %")

        st.progress(min(utilization / 100, 1.0))

        if utilization >= 100:
            st.error("🚨 Budget exceeded. Immediate action required.")
        elif utilization >= 80:
            st.warning("⚠️ Budget utilization above 80%. Monitor closely.")
        else:
            st.success("✅ Budget utilization within safe range.")

    # =================================================
    # EXPORT
    # =================================================
    with st.container(border=True):
        st.subheader("⬇️ Export")

        details_df = pd.DataFrame(st.session_state.cost_rows)
        st.download_button(
            "Download Cost Details CSV",
            details_df.to_csv(index=False).encode("utf-8"),
            "project_cost_details.csv",
            "text/csv",
        )

        summary_df = pd.DataFrame([{
            "Client Budget": client_budget,
            "Budget Currency": client_currency,
            "Total Internal Cost": total_internal,
            "Budget Utilization %": round(utilization, 2),
        }])

        st.download_button(
            "Download Budget Summary CSV",
            summary_df.to_csv(index=False).encode("utf-8"),
            "project_budget_summary.csv",
            "text/csv",
        )

else:
    st.info("No internal costs added yet.")
