import streamlit as st
import requests
from PIL import Image
from docx import Document
from io import BytesIO
from fpdf import FPDF

# --- Page Configuration ---
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- API Endpoint ---
API_URL = "http://localhost:8000/api/generate"

# --- Helper Functions for File Export ---
def create_docx(text: str) -> BytesIO:
    """Converts raw text into a downloadable Word (.docx) file."""
    doc = Document()
    for paragraph in text.split("\n\n"):
        doc.add_paragraph(paragraph)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def create_pdf(text: str) -> BytesIO:
    """Converts raw text into a downloadable PDF file."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Handle multi-line text and basic UTF-8 encoding
    for line in text.split("\n"):
        encoded_line = line.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, txt=encoded_line)
        
    pdf_output = pdf.output(dest='S')
    buffer = BytesIO(pdf_output.encode('latin-1'))
    return buffer


# --- Sidebar Setup ---
st.sidebar.title("Navigation & Branding")

# Load logo dynamically with fallback
try:
    logo = Image.open("Image/Logo.png")
    st.sidebar.image(logo, use_column_width=True)
except Exception:
    st.sidebar.info("📂 LegalEase Platform")

st.sidebar.markdown("---")
st.sidebar.subheader("Document Settings")

doc_type = st.sidebar.selectbox(
    "Select Document Type",
    ["Non-Disclosure Agreement (NDA)", "Service Contract", "Employment Agreement", "Custom Legal Document"]
)

tone = st.sidebar.select_slider(
    "Document Tone",
    options=["Standard", "Strict / Formal", "Balanced", "Friendly"]
)

# --- Main Content UI ---
st.title("⚖️ LegalEase AI Assistant")
st.caption("AI-powered legal document generation and drafting platform.")

st.markdown("### Document Details")

with st.form("legal_doc_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        party_a = st.text_input("Party A (Issuer / Employer)", placeholder="e.g., Acme Corp")
    with col2:
        party_b = st.text_input("Party B (Recipient / Employee)", placeholder="e.g., John Doe")
        
    details = st.text_area(
        "Key Clauses & Context",
        height=180,
        placeholder="Enter key terms, compensation, jurisdiction, termination clauses, duration, etc."
    )
    
    submit_button = st.form_submit_button("Generate Document", use_container_width=True)

# --- Form Handling & API Call ---
if submit_button:
    if not details or not party_a or not party_b:
        st.warning("Please fill in both party names and the key clause details before generating.")
    else:
        # Prepare request payload
        payload = {
            "doc_type": doc_type,
            "details": {
                "party_a": party_a,
                "party_b": party_b,
                "tone": tone,
                "context": details
            }
        }
        
        with st.spinner("Drafting document via Gemini AI..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json().get("content", "")
                    st.session_state["generated_doc"] = result
                    st.success("Document generated successfully!")
                else:
                    st.error(f"Error {response.status_code}: Unable to generate document.")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the LegalEase API backend. Ensure `main.py` is running on port 8000.")

# --- Render Results & Export Options ---
if "generated_doc" in st.session_state and st.session_state["generated_doc"]:
    st.markdown("---")
    st.subheader("Generated Document Preview")
    
    # Text display area
    edited_doc = st.text_area(
        "Edit your draft below befor downloading:"
    )