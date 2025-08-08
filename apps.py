import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="📚 AI Study Assistant", layout="centered")

st.title("📖 Personalized AI Study Assistant")

uploaded_file = st.file_uploader("Upload your notes or textbook (PDF)", type="pdf")

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF loaded!")

    if st.button("🔍 Summarize Chapter"):
        with st.spinner("Summarizing..."):
            summary = model.generate_content(f"Summarize this textbook chapter:\n\n{text[:7000]}").text
        st.subheader("📚 Summary")
        st.write(summary)

    if st.button("📝 Generate Quiz Questions"):
        with st.spinner("Generating..."):
            quiz = model.generate_content(f"Create 5 quiz questions (MCQ, T/F, Short answer) from:\n\n{text[:7000]}").text
        st.subheader("🧠 Quiz Questions")
        st.write(quiz)

    question = st.text_input("💬 Ask a question based on the notes:")
    if question:
        with st.spinner("Thinking..."):
            answer = model.generate_content(f"Answer this question based on the notes:\n\n{text[:7000]}\n\nQuestion: {question}").text
        st.subheader("💡 Answer")
        st.write(answer)
