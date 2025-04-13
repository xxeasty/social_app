import streamlit as st

def hide_sidebar():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        position: absolute !important;
        top: -100px !important;
    }
    </style>
    """, unsafe_allow_html=True)