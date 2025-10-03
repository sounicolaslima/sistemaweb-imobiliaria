# theme.py
import streamlit as st

def apply_theme():
    """Aplica o tema claro/escuro de forma adaptativa em todo o sistema"""
    
    # Verificar o tema atual do Streamlit
    try:
        # Tenta detectar o tema do Streamlit
        theme = st.get_option("theme.base")
        is_dark = theme == "dark"
    except:
        # Fallback para detectar tema
        try:
            # Verifica cores do tema
            background_color = st.get_option("theme.backgroundColor")
            is_dark = background_color == "#0E1117"
        except:
            # Default para tema claro
            is_dark = False
    
    # Cores adaptativas baseadas no tema
    if is_dark:
        # TEMA ESCURO
        primary_bg = "#0E1117"
        secondary_bg = "#262730"
        text_color = "#FAFAFA"
        border_color = "#555555"
        accent_color = "#4CAF50"
        card_bg = "#1E1E1E"
        hover_bg = "#2A2A2A"
        button_bg = "#2A2A2A"
        button_hover = "#3A3A3A"
    else:
        # TEMA CLARO
        primary_bg = "#FFFFFF"
        secondary_bg = "#F0F2F6"
        text_color = "#31333F"
        border_color = "#DCDCDC"
        accent_color = "#4CAF50"
        card_bg = "#FFFFFF"
        hover_bg = "#F8F9FA"
        button_bg = "#F8F9FA"
        button_hover = "#E9ECEF"
    
    st.markdown(f"""
    <style>
    /* ===== VARIÁVEIS CSS PARA TEMA CLARO/ESCURO ===== */
    :root {{
        --primary-bg: {primary_bg};
        --secondary-bg: {secondary_bg};
        --text-color: {text_color};
        --border-color: {border_color};
        --accent-color: {accent_color};
        --card-bg: {card_bg};
        --hover-bg: {hover_bg};
        --button-bg: {button_bg};
        --button-hover: {button_hover};
    }}
    
    /* ===== ESTILOS GLOBAIS ===== */
    .main-container, .main-dashboard-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: var(--primary-bg);
        color: var(--text-color);
    }}
    
    /* ===== SEÇÕES E HEADERS ===== */
    .section-header {{
        text-align: center;
        margin: 25px 0 15px 0;
        padding: 12px;
        background-color: var(--secondary-bg);
        border-radius: 8px;
        border-left: 4px solid var(--accent-color);
        color: var(--text-color);
    }}
    
    .comodo-container {{
        background-color: var(--secondary-bg);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid var(--accent-color);
        color: var(--text-color);
    }}
    
    /* ===== CARDS E BOTÕES ===== */
    .card-button, .planilha-button {{
        background-color: var(--card-bg);
        border: 2px solid var(--border-color);
        border-radius: 10px;
        padding: 25px 15px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: var(--text-color) !important;
    }}
    
    .card-button:hover, .planilha-button:hover {{
        border-color: var(--accent-color);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        background-color: var(--hover-bg);
    }}
    
    /* ===== FORMULÁRIOS E INPUTS ===== */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {{
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }}
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {{
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 2px {accent_color}20 !important;
    }}
    
    /* Labels dos inputs */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stNumberInput label, .stDateInput label {{
        color: var(--text-color) !important;
        font-weight: 500;
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
    
    /* ===== TABELAS E DADOS ===== */
    .dataframe {{
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
    }}
    
    /* ===== INFO, SUCESSO, AVISOS ===== */
    .stAlert {{
        background-color: var(--secondary-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }}
    
    /* ===== BOTÕES DO STREAMLIT - ESTILO ORIGINAL ===== */
    .stButton > button {{
        background-color: var(--button-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        font-weight: 400 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        background-color: var(--button-hover) !important;
        border-color: var(--accent-color) !important;
        color: var(--text-color) !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    /* Botão primário (apenas para botões específicos) */
    .stButton > button[data-testid*="primary"] {{
        background-color: var(--accent-color) !important;
        color: white !important;
        border: none !important;
    }}
    
    .stButton > button[data-testid*="primary"]:hover {{
        background-color: {accent_color}DD !important;
        color: white !important;
    }}
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--secondary-bg);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--border-color);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--accent-color);
    }}
    
    /* ===== LOGO - FORÇAR VISIBILIDADE ===== */
    .logo-container img {{
        filter: none !important;
        background: transparent !important;
    }}
    
    /* ===== TEXTO GERAL ===== */
    body {{
        background-color: var(--primary-bg);
        color: var(--text-color);
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-color) !important;
    }}
    
    p, div, span {{
        color: var(--text-color) !important;
    }}
    
    /* ===== USER INFO ===== */
    .user-info {{
        background-color: var(--secondary-bg);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid var(--accent-color);
        margin-bottom: 15px;
        color: var(--text-color);
    }}
    
    /* ===== FRASE DO DIA ===== */
    .frase-container {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    
    .frase-titulo, .frase-texto, .data-atual {{
        color: white !important;
    }}
    
    /* ===== LINHAS DIVISÓRIAS ===== */
    hr {{
        border-color: var(--border-color) !important;
    }}
    
    /* ===== PLACEHOLDERS ===== */
    ::placeholder {{
        color: {text_color}80 !important;
    }}
    
    /* ===== OVERRIDES ESPECÍFICOS PARA COMPATIBILIDADE ===== */
    .st-bb, .st-at, .st-ae, .st-af, .st-ag, .st-ah, .st-ai, .st-aj {{
        color: var(--text-color) !important;
    }}
    
    </style>
    """, unsafe_allow_html=True)
    
    # CSS adicional para garantir compatibilidade
    st.markdown("""
    <style>
        /* Garante que todos os textos sejam visíveis */
        .st-emotion-cache-1kyxreq, .st-emotion-cache-1v0mbdj, .st-emotion-cache-1y4p8pa {
            color: inherit !important;
        }
        
        /* Remove qualquer fundo branco forçado */
        .stApp {
            background-color: var(--primary-bg) !important;
        }
        
        /* Sidebar */
        .st-emotion-cache-1cypcdb {
            background-color: var(--secondary-bg) !important;
        }
        
        /* Botões do formulário - estilo original */
        div[data-testid="stForm"] .stButton > button {
            background-color: var(--button-bg) !important;
            color: var(--text-color) !important;
            border: 1px solid var(--border-color) !important;
        }
        
        div[data-testid="stForm"] .stButton > button:hover {
            background-color: var(--button-hover) !important;
            border-color: var(--accent-color) !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Função auxiliar para verificar tema
def is_dark_theme():
    """Retorna True se o tema for escuro"""
    try:
        theme = st.get_option("theme.base")
        return theme == "dark"
    except:
        return False