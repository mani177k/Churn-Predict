import os
import sys
from pathlib import Path

# Robust path handling for local and cloud deployment
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from scripts.predict import predict_churn

st.set_page_config(
    page_title="ChurnPredict | Intelligence Dashboard",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        * { font-family: 'Inter', sans-serif; }
        
        .stDeployButton, #MainMenu, [data-testid="stStatusWidget"], [data-testid="stDecoration"] { 
            display: none !important; 
        }
        header a { display: none !important; }
        footer { visibility: hidden !important; }
        
        header { 
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
        }
        .block-container { 
            padding-top: 0rem !important; 
            margin-top: 0rem !important; 
        }
        
        [data-testid="stHeader"] button:first-child { 
            visibility: visible !important; 
            display: inline-flex !important;
            position: fixed !important;
            top: 15px !important;
            left: 15px !important;
            z-index: 999999 !important;
            background-color: #ffffff !important;
            border-radius: 50% !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }
        
        .stApp { background-color: #f1f5f9 !important; color: #1a202c !important; }
        [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #edf2f7 !important; }
        
        .metric-card {
            background-color: #ffffff !important;
            padding: 24px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
            border: 1px solid #edf2f7 !important;
            text-align: center !important;
            margin-bottom: 1rem !important;
        }
        .metric-label { font-size: 13px; font-weight: 600; color: #718096 !important; text-transform: uppercase; letter-spacing: 0.05em; }
        .metric-value { font-size: 28px; font-weight: 800; color: #1a202c !important; margin-top: 6px; }
        
        button[kind="primary"] {
            background-color: #FF4D4D !important;
            color: white !important;
            width: auto !important;
            min-width: 280px !important;
            padding: 12px 30px !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 700 !important;
            display: block !important;
            margin: 0 auto !important;
            white-space: nowrap !important;
        }
        button[kind="secondary"] {
            background-color: #000000 !important;
            color: #ffffff !important;
            width: auto !important;
            min-width: 240px !important;
            padding: 10px 25px !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            display: block !important;
            margin: 0 auto !important;
            white-space: nowrap !important;
        }

        button[kind="primary"]:hover { background-color: #E64545 !important; box-shadow: 0 4px 12px rgba(255, 77, 77, 0.3) !important; }
        button[kind="secondary"]:hover { background-color: #333333 !important; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important; }
        
        [data-testid="stSidebar"] button[kind="secondary"] {
            width: 100% !important;
            margin-bottom: 10px !important;
        }
        
        [data-testid="stSidebar"] h2 {
            font-size: 1.8rem !important;
            font-weight: 800 !important;
            margin-bottom: 0px !important;
        }

        [data-testid="stSidebar"] .stRadio > div {
            gap: 15px !important;
        }
        
        [data-testid="stFileUploader"] {
            margin-bottom: 15px !important;
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:last-child button {
            background-color: #f1f3f5 !important;
            border: 1px solid #ff4b4b !important;
            color: #ff4b4b !important;
            font-weight: 700 !important;
        }
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:last-child button:hover {
            background-color: #e9ecef !important;
        }

        .block-container { padding-top: 0rem !important; }
        
        [data-testid="InputInstructions"] { display: none !important; }
        
        .login-header { text-align: center; margin-bottom: 2rem; }
        .login-header h1 { font-size: 3rem !important; font-weight: 800 !important; color: #1a202c !important; margin-bottom: 0px !important; }
        .login-header p { color: #718096 !important; font-size: 1.1rem; margin-top: 0px !important; }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 5px solid #000000 !important;
            border-radius: 12px !important;
            box-shadow: 0 30px 70px rgba(0,0,0,0.25) !important;
            background-color: #ffffff !important;
            padding: 3.5rem !important;
            max-width: 480px !important;
            margin: 0 auto !important;
            visibility: visible !important;
            display: block !important;
        }

        .login-card-header { text-align: center; margin-bottom: 2.5rem; }
        .login-card-header h1 { font-size: 2.8rem !important; font-weight: 900 !important; color: #1a202c !important; margin-bottom: 5px !important; }
        .login-card-header p { color: #2d3748 !important; font-size: 1.1rem; font-weight: 600 !important; margin-top: 0px !important; }

        .stTextInput, .stButton {
            max-width: 350px !important;
            margin: 0 auto !important;
        }
        .stTextInput label {
            text-align: left !important;
            display: block !important;
            width: 100% !important;
            color: #4a5568 !important;
            font-weight: 600 !important;
            margin-bottom: 8px !important;
            padding-left: 2px !important;
        }

        .stTextInput input {
            border-radius: 8px !important;
            border: 1px solid #e2e8f0 !important;
            padding: 12px 15px !important;
            background-color: #ffffff !important;
            text-align: left !important;
        }
        .stTextInput input:focus {
            border-color: #FF4D4D !important;
            box-shadow: 0 0 0 2px rgba(255, 77, 77, 0.1) !important;
            background-color: #ffffff !important;
        }
        
        .stTextInput button[aria-label="Show password"] {
            top: 50% !important;
            transform: translateY(-50%) !important;
            right: 10px !important;
        }

        .stButton { display: flex; justify-content: center; }

        /* ============================================================
           RESPONSIVE BREAKPOINTS — TABLET (max 1024px)
        ============================================================ */
        @media (max-width: 1024px) {
            .block-container {
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
            }
            .metric-card {
                padding: 18px !important;
            }
            .metric-value {
                font-size: 22px !important;
            }
            button[kind="primary"] {
                min-width: 200px !important;
                padding: 10px 20px !important;
            }
            button[kind="secondary"] {
                min-width: 180px !important;
                padding: 9px 18px !important;
            }
        }

        /* ============================================================
           RESPONSIVE BREAKPOINTS — MOBILE (max 768px)
        ============================================================ */
        @media (max-width: 768px) {

            /* Global container */
            .block-container {
                padding-left: 0.75rem !important;
                padding-right: 0.75rem !important;
                padding-bottom: 2rem !important;
            }

            /* Page titles */
            h1 { font-size: 1.6rem !important; }
            h2 { font-size: 1.3rem !important; }
            h3 { font-size: 1.1rem !important; }
            h4 { font-size: 1rem !important; }

            /* ---- Login Card ---- */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                padding: 2rem 1.25rem !important;
                max-width: 100% !important;
                border-radius: 10px !important;
                border-width: 3px !important;
                box-shadow: 0 8px 30px rgba(0,0,0,0.15) !important;
            }
            .login-card-header h1 {
                font-size: 2rem !important;
            }
            .login-card-header p {
                font-size: 0.95rem !important;
            }
            .stTextInput, .stButton {
                max-width: 100% !important;
            }

            /* ---- KPI Cards: stack 2-per-row then 1-per-row ---- */
            .metric-card {
                padding: 14px !important;
                margin-bottom: 0.75rem !important;
            }
            .metric-label {
                font-size: 11px !important;
            }
            .metric-value {
                font-size: 20px !important;
            }

            /* ---- Plotly Charts: preserve aspect ratio ---- */
            .js-plotly-plot, .plotly, .plot-container {
                width: 100% !important;
                min-width: 0 !important;
                overflow: hidden !important;
            }
            .stPlotlyChart {
                width: 100% !important;
                overflow-x: hidden !important;
            }

            /* ---- Tables: horizontal scroll ---- */
            .stTable, [data-testid="stTable"], .stDataFrame {
                display: block !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
                white-space: nowrap !important;
                max-width: 100% !important;
            }
            [data-testid="stDataFrame"] > div {
                overflow-x: auto !important;
            }

            /* ---- Buttons: full width on mobile ---- */
            button[kind="primary"] {
                width: 100% !important;
                min-width: unset !important;
                max-width: 100% !important;
                padding: 12px 16px !important;
                font-size: 0.95rem !important;
            }
            button[kind="secondary"] {
                width: 100% !important;
                min-width: unset !important;
                max-width: 100% !important;
                padding: 10px 14px !important;
                font-size: 0.9rem !important;
            }

            /* ---- Inputs: full width, tap-friendly ---- */
            .stTextInput input,
            .stSelectbox select,
            .stNumberInput input {
                font-size: 16px !important;
                padding: 12px !important;
            }

            /* ---- Columns: force single-column stacking ---- */
            [data-testid="column"] {
                min-width: 100% !important;
                flex: 1 1 100% !important;
            }

            /* ---- Sidebar toggle remains fixed and accessible ---- */
            [data-testid="stHeader"] button:first-child {
                top: 10px !important;
                left: 10px !important;
                width: 38px !important;
                height: 38px !important;
            }

            /* ---- File uploader ---- */
            [data-testid="stFileUploader"] {
                width: 100% !important;
            }

            /* ---- Slider: prevent overflow ---- */
            .stSlider {
                width: 100% !important;
                overflow: hidden !important;
            }

            /* ---- Prevent horizontal scroll on the whole page ---- */
            .stApp, .main, .block-container {
                overflow-x: hidden !important;
                max-width: 100vw !important;
            }
        }

        /* ============================================================
           RESPONSIVE BREAKPOINTS — SMALL MOBILE (max 480px)
        ============================================================ */
        @media (max-width: 480px) {
            div[data-testid="stVerticalBlockBorderWrapper"] {
                padding: 1.5rem 1rem !important;
            }
            .login-card-header h1 {
                font-size: 1.7rem !important;
            }
            .metric-value {
                font-size: 18px !important;
            }
            h1 { font-size: 1.4rem !important; }
        }
        </style>
    """, unsafe_allow_html=True)

def init_session_state():
    params = st.query_params.to_dict()
    if params.get("logged_in") == "true":
        st.session_state["authenticated"] = True
    elif "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
            
    if "data" not in st.session_state:
        st.session_state["data"] = None
    if "mapping" not in st.session_state:
        st.session_state["mapping"] = None

def handle_login(email, password):
    if email == "admin@gmail.com" and password == "admin@123":
        st.session_state["authenticated"] = True
        st.query_params["logged_in"] = "true"
        st.rerun()
    else:
        st.error("Invalid credentials")

def handle_logout():
    st.session_state["authenticated"] = False
    st.query_params.clear()
    if "logged_in" in st.query_params:
        del st.query_params["logged_in"]
    st.session_state.clear()
    st.rerun()

def render_login_page():
    apply_custom_css()
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("""
                <div class='login-card-header'>
                    <h1>ChurnPredict</h1>
                    <p>Customer Retention Intelligence</p>
                </div>
            """, unsafe_allow_html=True)
            email = st.text_input("Email address", placeholder="Enter your email", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
            st.markdown("<div style='margin-top: 35px;'></div>", unsafe_allow_html=True)
            if st.button("Sign In", use_container_width=True, type="primary"):
                handle_login(email, password)

def kpi_card(label, value, color="#1a202c"):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color: {color}">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def render_dashboard_panel():
    st.title("Analytics Dashboard")
    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

    if st.session_state["data"] is None:
        st.info("Please upload a customer dataset in the sidebar to begin analysis.")
        return

    df = st.session_state["data"]
    if st.session_state["mapping"] is None:
        st.markdown("### Feature Mapping")
        cols = df.columns.tolist()
        m = {}
        c1, c2 = st.columns(2, gap="large")
        with c1:
            m["Churn"] = st.selectbox("Churn Column", cols, index=cols.index("Churn") if "Churn" in cols else 0)
            m["Tenure"] = st.selectbox("Tenure Column", cols, index=cols.index("Tenure") if "Tenure" in cols else 0)
        with c2:
            m["MonthlyCharges"] = st.selectbox("Monthly Charges Column", cols, index=cols.index("MonthlyCharges") if "MonthlyCharges" in cols else 0)
            m["ContractType"] = st.selectbox("Contract Type Column", cols, index=cols.index("ContractType") if "ContractType" in cols else 0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        _, btn_col, _ = st.columns([1, 1.5, 1])
        with btn_col:
            if st.button("Confirm & Generate Dashboard", key="confirm_map", type="secondary"):
                st.session_state["mapping"] = m
                st.rerun()
        return

    m = st.session_state["mapping"]
    churn_rate = (df[m["Churn"]].map({'Yes': 1, 'No': 0, '1': 1, '0': 0, 1: 1, 0: 0}).mean()) * 100
    avg_charges = df[m["MonthlyCharges"]].mean()
    
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1: kpi_card("Total Customers", f"{len(df):,}")
    with k2: kpi_card("Average Churn", f"{churn_rate:.1f}%", color="#e53e3e" if churn_rate > 20 else "#38a169")
    with k3: kpi_card("Avg Monthly Rev", f"₹{avg_charges:,.0f}")
    with k4: kpi_card("High Risk Customers", f"{int(len(df) * (churn_rate/100)):,}", color="#dd6b20")

    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("#### Feature Impact on Churn")
        try:
            with open(os.path.join(base_dir, "models", "feature_importance.json"), "r") as f:
                feat_imp = json.load(f)
                impact_data = pd.DataFrame(feat_imp).head(5)
                impact_data.columns = ["Feature", "Impact"]
        except:
            impact_data = pd.DataFrame({"Feature": ["Contract", "Charges", "Tenure", "Payment", "Gender"], "Impact": [0.45, 0.25, 0.15, 0.10, 0.05]})
        
        fig = px.bar(impact_data, x="Impact", y="Feature", orientation='h', color_discrete_sequence=['#1a202c'])
        fig.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.markdown("#### Tenure vs Monthly Charges")
        fig = px.scatter(df, x=m["Tenure"], y=m["MonthlyCharges"], color=m["Churn"], opacity=0.6, color_discrete_map={"Yes": "#e53e3e", "No": "#38a169"})
        fig.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2, gap="large")
    with c3:
        st.markdown("#### Churn Rate by Contract Type")
        churn_by_contract = df.groupby(m["ContractType"])[m["Churn"]].apply(lambda x: (x.map({'Yes':1,'No':0,'1':1,'0':0,1:1,0:0}).mean()*100)).reset_index()
        churn_by_contract.columns = ["Contract", "Churn Rate %"]
        fig = px.bar(churn_by_contract, x="Contract", y="Churn Rate %", color="Contract", color_discrete_sequence=px.colors.qualitative.Safe)
        fig.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown("#### Payment Method Distribution")
        pm_col = "PaymentMethod" if "PaymentMethod" in df.columns else df.columns[0]
        fig = px.pie(df, names=pm_col, hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    st.markdown("#### Risk Segmentation Summary")
    risk_summary = df.groupby(m["ContractType"]).agg({m["Churn"]: "count", m["MonthlyCharges"]: "mean"}).reset_index()
    risk_summary.columns = ["Segment", "Total Customers", "Avg Monthly Revenue"]
    st.table(risk_summary)

    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
    
    st.markdown("#### 🚨 High Risk Customers Segment")
    high_risk_df = df[df[m["Churn"]].astype(str).str.lower().isin(['yes', '1', 'true'])].copy()
    if not high_risk_df.empty:
        high_risk_df.index = range(1, len(high_risk_df) + 1)
        st.dataframe(high_risk_df.head(20), use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        _, btn_col, _ = st.columns([1, 1.2, 1])
        with btn_col:
            st.download_button(
                label="📥 Export Customers (CSV)",
                data=high_risk_df.to_csv(index=False),
                file_name="high_risk_customers.csv",
                mime="text/csv",
                key="export_btn",
                type="secondary"
            )

def render_prediction_panel():
    st.title("Prediction Intelligence")
    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
    l, r = st.columns([1, 1.2], gap="large")
    
    with l:
        st.markdown("#### Profile Input")
        with st.container(border=True):
            gender = st.selectbox("Gender", ["Male", "Female"])
            tenure = st.slider("Tenure (Months)", 0, 72, 12)
            contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
            monthly_charges = st.number_input("Monthly Charges (₹)", min_value=15.0, value=70.0)
            payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            _, btn_col, _ = st.columns([1, 1.2, 1])
            with btn_col:
                if st.button("Analyze Risk", key="analyze_risk", type="primary"):
                    data = {"Gender": gender, "Tenure": tenure, "ContractType": contract, "MonthlyCharges": monthly_charges, "PaymentMethod": payment}
                    with st.spinner("Processing AI Analysis..."):
                        st.session_state["prediction_result"] = predict_churn(data)

    with r:
        st.markdown("#### Risk Insight")
        if st.session_state.get("prediction_result"):
            res = st.session_state["prediction_result"]
            prob = res["probability"]
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = prob * 100,
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#1a202c"},
                         'steps': [{'range': [0, 40], 'color': "#38a169"},
                                   {'range': [40, 70], 'color': "#dd6b20"},
                                   {'range': [70, 100], 'color': "#e53e3e"}]}))
            fig.update_layout(height=280, margin=dict(t=30, b=0, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"**Risk Severity:** {res['risk_level']}")
            st.markdown("---")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Key Risk Factors**")
                for reason in res["reasons"]: st.info(f"💡 {reason}")
            with c2:
                st.markdown("**Retention Plan**")
                for rec in res["recommendations"]: st.success(f"✅ {rec}")
        else:
            st.info("Select customer profile and run analysis.")

def main():
    init_session_state()
    apply_custom_css()
    if not st.session_state["authenticated"]:
        render_login_page()
    else:
        st.sidebar.markdown("<h2 style='text-align: center;'>ChurnPredict</h2>", unsafe_allow_html=True)
        st.sidebar.markdown("---")
        
        nav = st.sidebar.radio("NAVIGATE", ["Intelligence Panel", "Analytics Dashboard"], label_visibility="collapsed")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Data Management")
        up = st.sidebar.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        if up:
            st.session_state["data"] = pd.read_csv(up)
            st.sidebar.success(f"Active: {up.name}")
            if st.sidebar.button("Replace Dataset", use_container_width=True):
                st.session_state["data"] = None
                st.session_state["mapping"] = None
                st.rerun()
        
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
        if st.sidebar.button("Logout", use_container_width=True, key="logout_sidebar"):
            handle_logout()
            
        if nav == "Intelligence Panel":
            render_prediction_panel()
        else:
            render_dashboard_panel()

if __name__ == "__main__":
    main()
