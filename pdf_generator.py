from fpdf import FPDF
from typing import Dict, Any, List

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PRIME CVD Risk Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(
    patient_data: Dict[str, Any],
    risk_data: Dict[str, Any],
    ldl_history: List[float]
) -> bytes:
    """
    Generate a PDF report with patient risk assessment.
    
    Args:
        patient_data: Dictionary with patient demographics
        risk_data: Dictionary with risk factors and scores
        ldl_history: List of historical LDL values
        
    Returns:
        bytes: PDF file content
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # Patient information
    pdf.cell(0, 10, f"Patient: {patient_data['sex']}, {patient_data['age']} years", 0, 1)
    pdf.ln(5)
    
    # Risk summary
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"10-Year CVD Risk: {patient_data['risk_score']}%", 0, 1)
    pdf.set_font('Arial', '', 12)
    
    # Risk factors
    pdf.ln(5)
    pdf.cell(0, 10, "Major Risk Factors:", 0, 1)
    pdf.cell(0, 10, f"- Age: {risk_data['factors']['age']} years", 0, 1)
    pdf.cell(0, 10, f"- Blood Pressure: {risk_data['factors']['sbp']} mmHg", 0, 1)
    pdf.cell(0, 10, f"- Total Cholesterol: {risk_data['factors']['cholesterol']} mmol/L", 0, 1)
    pdf.cell(0, 10, f"- HDL Cholesterol: {risk_data['factors']['hdl']} mmol/L", 0, 1)
    
    return pdf.output(dest='S').encode('latin1')