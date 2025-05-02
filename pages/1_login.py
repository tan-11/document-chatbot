import streamlit as st
import os
import sys
from helper.db_helper import create_tables
from streamlit_lottie import st_lottie
import requests



st.set_page_config(page_title="🔐 Login | AI Chatbot", layout="centered")

st.title("👋 Welcome to SmartDocBot!")
st.subheader("Your AI-powered assistant for exploring documents 📄✨")
st.markdown("Please **log in** to get started.")

user_id = st.text_input("Enter your User ID to login: ")

st.markdown("""
    <style>
    .stApp {
        background-image: url('http://www.transparenttextures.com/patterns/tileable-wood.png');
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)



if st.button("Login") and user_id:
    st.session_state.new_user_id = user_id
    st.write(f"Hi, {user_id}Welcome to AI Chatbot!!!")  # Switch to the chatbot page
