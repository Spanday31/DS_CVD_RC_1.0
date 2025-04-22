import streamlit as st
from datetime import datetime
from calculations import calculate_smart_risk
from utils import load_logo
from pdf_generator import create_pdf_report

# Page configuration
st.set_page_config(
    page_title="PRIME CVD Risk Calculator",
    layout="wide",
    page_icon="❤️",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .risk-high { color: #ff4b4b !important; font-weight: bold; }
        .risk-medium { color: #ffa500 !important; font-weight: bold; }
        .risk-low { color: #0c9d58 !important; font-weight: bold; }
        .sidebar .sidebar-content { background-color: #f8f9fa; }
        div[data-testid="stSidebarUserContent"] { padding: 1rem; }
    </style>
""", unsafe_allow_html=True)

# Header with logo
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("""<div style='background:linear-gradient(135deg,#3b82f6,#2563eb);padding:1rem;border-radius:10px;'>
        <h1 style='color:white;margin:0;'>PRIME CVD Risk Calculator</h1>
        <p style='color:#e0f2fe;margin:0;'>Secondary Prevention After Myocardial Infarction</p>
    </div>""", unsafe_allow_html=True)
with col2:
    load_logo()

# Sidebar inputs
with st.sidebar:
    st.title("Patient Demographics")
    age = st.number_input(
        "Age (years)", 
        min_value=30, 
        max_value=100, 
        value=65,
        help="Patient age between 30-100 years"
    )
    sex = st.radio("Sex", ["Male", "Female"], horizontal=True)
    diabetes = st.checkbox("Diabetes mellitus")
    smoker = st.checkbox("Current smoker")
    
    st.title("Vascular Disease")
    cad = st.checkbox("Coronary artery disease (CAD)")
    stroke = st.checkbox("Cerebrovascular disease (Stroke/TIA)")
    pad = st.checkbox("Peripheral artery disease (PAD)")
    vasc_count = sum([cad, stroke, pad])
    
    st.title("Biomarkers")
    total_chol = st.number_input(
        "Total Cholesterol (mmol/L)", 
        min_value=2.0, 
        max_value=10.0, 
        value=5.0, 
        step=0.1
    )
    hdl = st.number_input(
        "HDL-C (mmol/L)", 
        min_value=0.5, 
        max_value=3.0, 
        value=1.0, 
        step=0.1
    )
    ldl = st.number_input(
        "LDL-C (mmol/L)", 
        min_value=0.5, 
        max_value=6.0, 
        value=3.5, 
        step=0.1,
        help="Low-density lipoprotein cholesterol"
    )
    sbp = st.number_input(
        "SBP (mmHg)", 
        min_value=90, 
        max_value=220, 
        value=140,
        help="Systolic blood pressure"
    )
    egfr = st.slider(
        "eGFR (mL/min/1.73m²)", 
        min_value=15, 
        max_value=120, 
        value=80,
        help="Estimated glomerular filtration rate"
    )
    crp = st.number_input(
        "hs-CRP (mg/L)", 
        min_value=0.1, 
        max_value=20.0, 
        value=2.0, 
        step=0.1,
        help="High-sensitivity C-reactive protein"
    )

# Validation
if ldl < hdl:
    st.sidebar.error("LDL-C cannot be lower than HDL-C!")
    st.stop()

# Main content area
tab1, tab2, tab3 = st.tabs(["Risk Calculation", "LDL Management", "Recommendations"])

with tab1:
    st.header("10-Year CVD Risk Assessment")
    
    if st.button("Calculate Risk", type="primary", key="calculate"):
        with st.spinner("Calculating risk..."):
            baseline_risk = calculate_smart_risk(
                age, sex, sbp, total_chol, hdl, 
                smoker, diabetes, egfr, crp, vasc_count
            )
            
            # Determine risk category
            if baseline_risk >= 20:
                risk_category = "high"
                interpretation = "High risk - intensive therapy recommended"
            elif baseline_risk >= 10:
                risk_category = "medium"
                interpretation = "Moderate risk - consider therapy"
            else:
                risk_category = "low"
                interpretation = "Low risk - maintain healthy lifestyle"
            
            # Display results
            st.markdown(f"""
                <div style='border-left:5px solid {'#ff4b4b' if risk_category == 'high' else '#ffa500' if risk_category == 'medium' else '#0c9d58'};
                    padding:1rem;background-color:#f8f9fa;border-radius:5px;margin-bottom:1rem;'>
                    <h3 style='margin-top:0;'>10-Year CVD Risk: <span class='risk-{risk_category}'>{baseline_risk}%</span></h3>
                    <p>{interpretation}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Risk factors breakdown
            st.subheader("Risk Factor Contributions")
            cols = st.columns(3)
            with cols[0]:
                st.metric("Age", f"{age} years")
                st.metric("Sex", sex)
            with cols[1]:
                st.metric("Blood Pressure", f"{sbp} mmHg")
                st.metric("Cholesterol", f"Total: {total_chol}, HDL: {hdl}")
            with cols[2]:
                st.metric("Other Factors", 
                    f"{'Smoker, ' if smoker else ''}{'Diabetes, ' if diabetes else ''}{vasc_count} vascular diseases")
            
            # Generate PDF report
            if st.button("Generate PDF Report"):
                pdf_data = create_pdf_report(
                    patient_data={
                        "age": age,
                        "sex": sex,
                        "risk_score": baseline_risk
                    },
                    risk_data={
                        "factors": {
                            "age": age,
                            "sbp": sbp,
                            "cholesterol": total_chol,
                            "hdl": hdl
                        }
                    },
                    ldl_history=[]
                )
                st.download_button(
                    label="Download Report",
                    data=pdf_data,
                    file_name=f"cvd_risk_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )

with tab2:
    st.header("LDL-C Management")
    st.info("LDL management features will be implemented in the next version")

with tab3:
    st.header("Personalized Recommendations")
    st.info("Recommendation engine will be implemented in the next version")