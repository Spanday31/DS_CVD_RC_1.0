import math
import streamlit as st

@st.cache_data
def calculate_smart_risk(
    age: int,
    sex: str,
    sbp: int,
    total_chol: float,
    hdl: float,
    smoker: bool,
    diabetes: bool,
    egfr: int,
    crp: float,
    vasc_count: int
) -> float:
    """
    Calculate 10-year CVD risk using SMART risk score algorithm.
    
    Args:
        age: Patient age in years (30-100)
        sex: "Male" or "Female"
        sbp: Systolic blood pressure (mmHg)
        total_chol: Total cholesterol (mmol/L)
        hdl: HDL cholesterol (mmol/L)
        smoker: Current smoking status
        diabetes: Diabetes mellitus diagnosis
        egfr: Estimated GFR (mL/min/1.73m²)
        crp: High-sensitivity CRP (mg/L)
        vasc_count: Count of vascular diseases (0-3)
        
    Returns:
        float: 10-year CVD risk percentage (0-100)
    """
    # Base coefficients (example values - replace with actual SMART model)
    coefficients = {
        'age': 0.04,
        'male': 0.7,
        'sbp': 0.02,
        'total_chol': 0.3,
        'low_hdl': -0.4,
        'smoker': 0.6,
        'diabetes': 0.8,
        'egfr<60': 0.5,
        'elevated_crp': 0.3,
        'vascular_disease': 0.4
    }
    
    # Calculate individual components
    risk_score = 0
    risk_score += age * coefficients['age']
    risk_score += coefficients['male'] if sex == "Male" else 0
    risk_score += sbp * coefficients['sbp']
    risk_score += total_chol * coefficients['total_chol']
    risk_score += coefficients['low_hdl'] if hdl < 1.0 else 0
    risk_score += coefficients['smoker'] if smoker else 0
    risk_score += coefficients['diabetes'] if diabetes else 0
    risk_score += coefficients['egfr<60'] if egfr < 60 else 0
    risk_score += coefficients['elevated_crp'] if crp > 2.0 else 0
    risk_score += vasc_count * coefficients['vascular_disease']
    
    # Convert to percentage (using inverse logit for example)
    risk_percent = 100 * (1 / (1 + math.exp(-risk_score)))
    
    return round(risk_percent, 1)