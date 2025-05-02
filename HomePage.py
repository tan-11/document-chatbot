import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="NLP Application",
    page_icon=":robot:",
    layout="wide"
)

# Main page content
st.title("Welcome to the SmartDocBot!")
st.subheader("Your AI-powered assistant for exploring documents 📄✨")
st.write("This is the main page of SmartDocBot. Use the navigation menu to access different features.")

st.write("""
Welcome to the Intelligent PDF Text Extractor & Search Tool
This application allows you to upload PDF documents and automatically extract both typed text and image-based text using advanced OCR (Optical Character Recognition). It uses natural language processing (NLP) techniques like BM25 ranking and semantic embeddings to help you:

🔍 Search and retrieve the most relevant chunks of information

🧠 Understand the content even when text is embedded inside images

💡 Find answers to your questions from complex documents quickly

Whether you're reviewing research papers, scanning official reports, or analyzing scanned books — this tool helps you interact with your documents intelligently.
""")

# Instructions for navigation
st.sidebar.title("Navigation")
st.sidebar.write("Use the sidebar to navigate to different pages.")

# Add a button to navigate to the Login page
if st.button("Go to Login"):
    st.session_state.user_id = None  # Clear any existing user session
    st.switch_page("pages/1_login.py")  # Switch to the login page