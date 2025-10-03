# theme.py
import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    /* TÍTULOS - brancos no escuro, pretos no claro */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color, #000000) !important;
    }
    
    /* Se estiver no tema escuro, força títulos brancos */
    @media (prefers-color-scheme: dark) {
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
    }
    
    /* Override do Streamlit para tema escuro */
    [data-testid="stAppViewContainer"] {
        background-color: var(--background-color, #FFFFFF) !important;
    }
    
    /* Textos normais se adaptam ao tema */
    .stMarkdown {
        color: var(--text-color, #000000) !important;
    }
    </style>
    """, unsafe_allow_html=True)