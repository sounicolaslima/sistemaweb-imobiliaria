# theme.py
import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    /* CSS que funciona em tema claro e escuro */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .section-header {
        text-align: center;
        margin: 25px 0 15px 0;
        padding: 12px;
        background-color: var(--secondary-background-color, #f0f2f6);
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        color: var(--text-color, #333);
    }
    
    .comodo-container {
        background-color: var(--secondary-background-color, #f8f9fa);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
    }
    
    /* 👇 ADICIONE ESTAS REGRAS PARA OS TÍTULOS */
    /* TÍTULOS - se adaptam ao tema */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color, #000000) !important;
    }
    
    .stTitle {
        color: var(--text-color, #000000) !important;
    }
    
    .stMarkdown h1,
    .stMarkdown h2, 
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown h5,
    .stMarkdown h6 {
        color: var(--text-color, #000000) !important;
    }
    
    /* Cores que se adaptam automaticamente */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    
    /* Labels dos inputs */
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: var(--text-color) !important;
    }
    </style>
    """, unsafe_allow_html=True)