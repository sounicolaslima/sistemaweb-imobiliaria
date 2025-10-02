import streamlit as st
from PIL import Image
import os
import json

# ----------------- Configuração da página -----------------
st.set_page_config(page_title="Dashboard Villares", layout="wide")

# ----------------- Estado inicial -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicial"

# ----------------- Carregar usuários do JSON -----------------
ARQUIVO_USUARIOS = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

usuarios = carregar_usuarios()

# ----------------- Função de Login -----------------
def login():
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        # Logo centralizado com tamanho reduzido
        if os.path.exists("villares.png"):
            logo = Image.open("villares.png")
            st.image(logo, width=280, use_container_width=True)  # Reduzido de 360 para 280

        # Título centralizado com menor margem
        st.markdown("<h3 style='text-align: center; margin: 15px 0;'>Sistema Villares Imóveis</h3>", unsafe_allow_html=True)
        
        # Campos centralizados
        user = st.text_input("Usuário", placeholder="Digite seu usuário", key="login_user")
        pwd = st.text_input("Senha", type="password", placeholder="Digite sua senha", key="login_pwd")
        
        # Espaçamento reduzido
        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
        
        # Botão centralizado
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            # CSS para botão mais compacto
            st.markdown("""
                <style>
                    div[data-testid="stButton"] > button {
                        background-color: #4CAF50;
                        color: white;
                        padding: 8px 20px;
                        border: none;
                        border-radius: 6px;
                        font-size: 14px;
                        font-weight: bold;
                        width: 100%;
                    }
                    div[data-testid="stButton"] > button:hover {
                        background-color: #45a049;
                    }
                </style>
            """, unsafe_allow_html=True)
            
            if st.button("Entrar", use_container_width=True, key="login_button"):
                if user in usuarios and usuarios[user] == pwd:
                    st.session_state.logged_in = True
                    st.session_state.usuario = user
                    st.success(f"Bem-vindo, {user}!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")

# ----------------- Função para mudar de página -----------------
def mudar_pagina(pagina):
    st.session_state.pagina = pagina

# ----------------- Dashboard -----------------
def dashboard():
    # Sidebar com usuário logado
    st.sidebar.markdown(f"👤 Logado como: **{st.session_state.usuario}**")
    if st.sidebar.button("Sair"):
        st.session_state.logged_in = False
        st.session_state.usuario = None
        st.rerun()

    if st.session_state.pagina == "inicial":
        col_logo, col_title = st.columns([1,4])
        with col_logo:
            if os.path.exists("villares.png"):
                logo = Image.open("villares.png")
                st.image(logo, width=200)
        with col_title:
            st.markdown("<h1 style='margin-top:30px'>📂 Central de Geradores de Documentos</h1>", unsafe_allow_html=True)
            st.markdown("### Villares Imobiliária", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Escolha o gerador que deseja usar:")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📄 Gerar Ficha Cadastral", key="ficha_cadastral"):
                mudar_pagina("ficha_cadastral")
            if st.button("📝 Gerar Contrato Administrativo", key="contrato_admin"):
                mudar_pagina("contrato_administrativo")

        with col2:
            if st.button("📃 Gerar Contrato", key="contrato"):
                mudar_pagina("contrato")
            if st.button("🏠 Gerar Ficha de Captação", key="ficha_captacao"):
                mudar_pagina("ficha_captacao")

        with col3:
            if st.button("📋 Gerar Termo de Vistoria", key="termo_vistoria"):
                mudar_pagina("termo_vistoria")
            if st.button("📄 Gerar Recibo", key="recibo"):
                mudar_pagina("recibo")

        # Planilhas, também sem fundo branco
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                """
                <div style='text-align:center; margin-top:10px'>
                    <a href='https://docs.google.com/spreadsheets/d/1BPwecYI9zenjxQniEGgkh7CqBOSjOATi3R-2IRot4ow/edit?gid=890601984#gid=890601984' target='_blank'
                       style='background-color:#4CAF50; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; font-size:16px;'>
                       Acessar Planilha de carta de imóveis
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_b:
            st.markdown(
                """
                <div style='text-align:center; margin-top:10px'>
                    <a href='https://docs.google.com/spreadsheets/d/1T4FRm4KUVQjD4aSg3Hn_FI6E0h_m8KbfaPGnlviXydI/edit?usp=sharing' target='_blank'
                       style='background-color:#4CAF50; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; font-size:16px;'>
                       Acessar Planilha Gestão Orçamentária - Pagar e Receber
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Chamando scripts
    else:
        st.button("⬅️ Voltar", on_click=lambda: mudar_pagina("inicial"))

        if st.session_state.pagina == "ficha_cadastral":
            import fichaCadastral
            fichaCadastral.app()
        elif st.session_state.pagina == "contrato_administrativo":
            import contratoAdministracao
            contratoAdministracao.app()
        elif st.session_state.pagina == "contrato":
            import contrato
            contrato.app()
        elif st.session_state.pagina == "ficha_captacao":
            import cadastroImovel
            cadastroImovel.app()
        elif st.session_state.pagina == "termo_vistoria":
            import termo_vistoria
            termo_vistoria.app()
        elif st.session_state.pagina == "recibo":
            import recibo
            recibo.app()

# ----------------- Execução -----------------
if not st.session_state.logged_in:
    login()
else:
    dashboard()

