import streamlit as st

def hide_sidebar():
    """
    Hide Streamlit's default sidebar to create a cleaner UI.
    """
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
