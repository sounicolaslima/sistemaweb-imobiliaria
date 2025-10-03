# theme.py
import streamlit as st

def apply_theme():
    """Aplica o tema claro/escuro mantendo TODOS os estilos originais"""
    
    # Detectar tema atual
    try:
        theme = st.get_option("theme.base")
        is_dark = theme == "dark"
    except:
        try:
            background_color = st.get_option("theme.backgroundColor")
            is_dark = background_color == "#0E1117"
        except:
            is_dark = False
    
    # Cores adaptativas
    if is_dark:
        primary_bg = "#0E1117"
        secondary_bg = "#262730" 
        text_color = "#FAFAFA"
        border_color = "#555555"
    else:
        primary_bg = "#FFFFFF"
        secondary_bg = "#F0F2F6"
        text_color = "#31333F"
        border_color = "#DCDCDC"
    
    st.markdown(f"""
    <style>
    /* ===== TEMA ADAPTATIVO - MANTÉM ESTILOS ORIGINAIS ===== */
    :root {{
        --primary-bg: {primary_bg};
        --secondary-bg: {secondary_bg};
        --text-color: {text_color};
        --border-color: {border_color};
    }}
    
    /* ===== FUNDOS E TEXTOS ===== */
    .stApp {{
        background-color: var(--primary-bg) !important;
    }}
    
    .main-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: var(--primary-bg);
        color: var(--text-color);
    }}
    
    body {{
        background-color: var(--primary-bg);
        color: var(--text-color);
    }}
    
    h1, h2, h3, h4, h5, h6, p, div, span {{
        color: var(--text-color) !important;
    }}
    
    /* ===== SEÇÕES ===== */
    .section-header {{
        text-align: center;
        margin: 25px 0 15px 0;
        padding: 12px;
        background-color: var(--secondary-bg);
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        color: var(--text-color);
    }}
    
    /* ===== INPUTS E FORMULÁRIOS ===== */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {{
        background-color: var(--primary-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }}
    
    .stTextInput label, .stTextArea label, .stSelectbox label {{
        color: var(--text-color) !important;
    }}
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {{
        background-color: var(--secondary-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }}
    
    .streamlit-expanderContent {{
        background-color: var(--primary-bg) !important;
        color: var(--text-color) !important;
    }}
    
    /* ===== COMPATIBILIDADE ===== */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {{
        background-color: var(--secondary-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }}
    
    /* BOTÕES MANTIDOS NO ESTILO ORIGINAL - NÃO ALTERAR */
    /* Containers específicos para evitar conflitos */
    .page-container {{
        background-color: var(--primary-bg);
        min-height: 100vh;
    }}
    </style>
    """, unsafe_allow_html=True)

def is_dark_theme():
    """Retorna True se o tema for escuro"""
    try:
        theme = st.get_option("theme.base")
        return theme == "dark"
    except:
        return False