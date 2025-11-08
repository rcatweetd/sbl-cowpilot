import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import io
import json

# === YOUR MAGIC KEY GOES HERE LATER (in Streamlit secrets) ===
genai.configure(api_key=st.secrets["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')

# === PAGE SETUP ===
st.set_page_config(page_title="aCOWtancy SBL Cowpilot", page_icon="Cow")
st.title("Cow aCOWtancy SBL Cowpilot")
st.caption("Your AI SBL Exam Cowpilot — Pre-Seen to Pass")

# === UPLOAD PDF ===
uploaded = st.file_uploader("Upload Pre-Seen PDF", type="pdf")

if uploaded and st.button("Analyze Pre-Seen"):
    with st.spinner("Cowpilot is analyzing..."):
        pdf = PdfReader(io.BytesIO(uploaded.read()))
        text = "".join([p.extract_text() or "" for p in pdf.pages])
        
        prompt = f"""
        You are an ACCA SBL expert. Analyze this pre-seen.
        Return **only clean JSON** with:
        - company_summary
        - pestel (dict)
        - swot (dict)
        - 4_exam_tasks (list of dict: task, marks)
        Text: {text[:25000]}
        """
        response = model.generate_content(prompt)
        try:
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            st.session_state.analysis = json.loads(clean_json)
            st.success("Analysis Complete!")
        except:
            st.error("AI didn't return JSON. Try again.")

# === SHOW RESULTS ===
if "analysis" in st.session_state:
    ana = st.session_state.analysis
    st.write(f"**Company**: {ana.get('company_summary', 'N/A')}")
    
    if st.button("Generate Mock Exam"):
        st.session_state.exam = ana.get("4_exam_tasks", [])

if "exam" in st.session_state:
    for i, task in enumerate(st.session_state.exam):
        st.write(f"**Task {i+1}**: {task.get('task', '')} [{task.get('marks', 0)} marks]")
        st.text_area("Your answer", key=f"ans{i}", height=120)
    
    if st.button("Submit for Marking"):
        st.write("Marking coming soon!")
