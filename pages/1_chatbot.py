import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
from utils.ui import hide_sidebar
from components.chat_logic import render_chatbot  # ✅ 공통 로직만 import

st.set_page_config(page_title="GPT 챗봇", layout="centered")
hide_sidebar()

client = OpenAI()

render_chatbot(client)