# theme.py
import streamlit as st

# theme.py
import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    /* FORÇA cores específicas para tema claro e escuro */
    
    /* TEMA CLARO (default) */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .section-header {
        text-align: center;
        margin: 25px 0 15px 0;
        padding: 12px;
        background-color: #f0f2f6;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        color: #333333;
    }
    
    .comodo-container {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
    }
    
    /* TÍTULOS - Pretos no tema claro */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    .stTitle, .stHeader {
        color: #000000 !important;
    }
    
    /* TEMA ESCURO - Override completo */
    @media (prefers-color-scheme: dark) {
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
        }
        
        .stTitle, .stHeader {
            color: #FFFFFF !important;
        }
        
        .section-header {
            background-color: #2d3748 !important;
            color: #FFFFFF !important;
        }
        
        .comodo-container {
            background-color: #4a5568 !important;
            color: #FFFFFF !important;
        }
    }
    
    /* Override específico do Streamlit dark theme */
    [data-testid="stAppViewContainer"] {
        background-color: white;
    }
    
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] h5,
    [data-testid="stAppViewContainer"] h6 {
        color: #000000 !important;
    }
    
    /* Se o Streamlit detectar tema escuro, aplica override */
    .stApp[data-theme="dark"] h1,
    .stApp[data-theme="dark"] h2, 
    .stApp[data-theme="dark"] h3,
    .stApp[data-theme="dark"] h4,
    .stApp[data-theme="dark"] h5,
    .stApp[data-theme="dark"] h6 {
        color: #FFFFFF !important;
    }
    
    /* Inputs - sempre legíveis */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
    }
    
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: #000000 !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)