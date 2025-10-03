import streamlit as st
from PIL import Image
import os
import json
import requests
from datetime import datetime
import hashlib

# ----------------- Configuração da página -----------------
st.set_page_config(page_title="Dashboard Villares", layout="wide", initial_sidebar_state="collapsed")

# ----------------- Estado inicial -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicial"
if "frase_do_dia" not in st.session_state:
    st.session_state.frase_do_dia = ""
if "data_frase" not in st.session_state:
    st.session_state.data_frase = ""

# ----------------- Carregar usuários do JSON -----------------
ARQUIVO_USUARIOS = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

usuarios = carregar_usuarios()

# ----------------- Função para buscar frase do dia -----------------
def buscar_frase_do_dia(usuario):
    data_hoje = datetime.now().strftime("%Y%m%d")
    seed = usuario + data_hoje
    hash_obj = hashlib.md5(seed.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    
    try:
        response = requests.get("https://api.quotable.io/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and "content" in data:
                frase = data["content"]
                autor = data.get("author", "Desconhecido")
                return f'"{frase}" - {autor}'
    except:
        pass
    
    frases_fallback = [
        "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
        "A persistência é o caminho do êxito.",
        "Não espere por oportunidades, crie-as.",
        "Cada cliente satisfeito é uma vitória conquistada.",
    ]
    
    indice = hash_int % len(frases_fallback)
    return frases_fallback[indice]

# ----------------- Função de Login -----------------
def login():
    col_left, col_center, col_right = st.columns([1, 3, 1])

    with col_center:
        if os.path.exists("villares.png"):
            logo = Image.open("villares.png")
            col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
            with col_img2:
                st.markdown('<div class="logo-container">', unsafe_allow_html=True)
                st.image(logo, width=380)
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<h4 style='text-align: center; margin: 5px 0 10px 0; font-size: 28px;'>Sistema Villares Imóveis</h4>", unsafe_allow_html=True)
        
        col_user1, col_user2, col_user3 = st.columns([1, 2, 1])
        with col_user2:
            user = st.text_input("", placeholder="👤 Usuário", key="login_user", label_visibility="collapsed")
        
        col_pwd1, col_pwd2, col_pwd3 = st.columns([1, 2, 1])
        with col_pwd2:
            pwd = st.text_input("", type="password", placeholder="🔒 Senha", key="login_pwd", label_visibility="collapsed")
        
        st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("Entrar", use_container_width=True, key="login_button"):
                if user in usuarios and usuarios[user] == pwd:
                    st.session_state.logged_in = True
                    st.session_state.usuario = user
                    
                    data_hoje = datetime.now().strftime("%Y%m%d")
                    if st.session_state.data_frase != data_hoje:
                        st.session_state.frase_do_dia = buscar_frase_do_dia(user)
                        st.session_state.data_frase = data_hoje
                    
                    st.success(f"Bem-vindo, {user}!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")

# ----------------- Função para mudar de página -----------------
def mudar_pagina(pagina):
    st.session_state.pagina = pagina
    st.rerun()

# ----------------- Aplicar tema -----------------
def aplicar_tema_dashboard():
    st.markdown("""
        <style>
            .main-dashboard-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .section-header {
                text-align: center;
                margin: 30px 0 20px 0;
                padding: 15px;
                background-color: var(--secondary-background-color, #f0f2f6);
                border-radius: 10px;
                border-left: 5px solid #4CAF50;
                color: var(--text-color, #333);
            }
            .card-button {
                background-color: var(--background-color, white);
                border: 2px solid var(--border-color, #e0e0e0);
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
                color: var(--text-color, #333) !important;
            }
            .card-button:hover {
                border-color: #4CAF50;
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            }
            .user-info {
                background-color: var(--secondary-background-color, #f8f9fa);
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #4CAF50;
                margin-bottom: 15px;
                color: var(--text-color, #333);
            }
            .frase-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 15px 0;
                text-align: center;
            }
            h1, h2, h3 {
                color: var(--text-color, #000000) !important;
            }
        </style>
    """, unsafe_allow_html=True)

# ----------------- Dashboard -----------------
def dashboard():
    aplicar_tema_dashboard()
    
    # Verificar se precisa atualizar a frase
    data_hoje = datetime.now().strftime("%Y%m%d")
    if st.session_state.data_frase != data_hoje:
        st.session_state.frase_do_dia = buscar_frase_do_dia(st.session_state.usuario)
        st.session_state.data_frase = data_hoje
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="user-info">', unsafe_allow_html=True)
        st.markdown(f"👤 **Usuário:** {st.session_state.usuario}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.frase_do_dia:
            st.markdown('<div class="frase-container">', unsafe_allow_html=True)
            st.markdown('<div class="frase-titulo">💫 FRASE DO DIA</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="frase-texto">{st.session_state.frase_do_dia}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="data-atual">{datetime.now().strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚪 Sair do Sistema", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.usuario = None
            st.session_state.frase_do_dia = ""
            st.session_state.data_frase = ""
            st.session_state.pagina = "inicial"
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Navegação")
        if st.button("🏠 Página Inicial", use_container_width=True):
            mudar_pagina("inicial")

    # PÁGINA INICIAL
    if st.session_state.pagina == "inicial":
        st.markdown('<div class="main-dashboard-container">', unsafe_allow_html=True)
        
        col_logo, col_title = st.columns([1, 3])
        with col_logo:
            if os.path.exists("villares.png"):
                logo = Image.open("villares.png")
                st.image(logo, width=300)
        with col_title:
           st.markdown("<h1 style='color: white !important;'>🏢 Central de Documentos</h1>", unsafe_allow_html=True)
           st.markdown("<h3 style='color: white !important;'>Villares Imobiliária</h3>", unsafe_allow_html=True)

        st.markdown("---")
        
        st.markdown('<div class="section-header"><h2>📄 GERADORES DE DOCUMENTOS</h2></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("**📄 FICHA CADASTRAL**\n\nCadastro completo de locatários", use_container_width=True, key="ficha_cadastral"):
                mudar_pagina("ficha_cadastral")
            if st.button("**📝 CONTRATO ADMINISTRATIVO**\n\nAdministração de imóveis", use_container_width=True, key="contrato_admin"):
                mudar_pagina("contrato_administrativo")

        with col2:
            if st.button("**📃 CONTRATO DE LOCAÇÃO**\n\nContrato padrão de aluguel", use_container_width=True, key="contrato"):
                mudar_pagina("contrato")
            if st.button("**🏠 FICHA DE CAPTAÇÃO**\n\nCadastro de imóveis", use_container_width=True, key="ficha_captacao"):
                mudar_pagina("ficha_captacao")

        with col3:
            if st.button("**📋 TERMO DE VISTORIA**\n\nVistoria de imóveis", use_container_width=True, key="termo_vistoria"):
                mudar_pagina("termo_vistoria")
            if st.button("**📄 RECIBO**\n\nEmitir recibos", use_container_width=True, key="recibo"):
                mudar_pagina("recibo")

        st.markdown("---")
        st.markdown('<div class="section-header"><h2>📊 PLANILHAS EXTERNAS</h2></div>', unsafe_allow_html=True)
        
        col_plan1, col_plan2 = st.columns(2)
        
        with col_plan1:
            st.markdown(
                """
                <div style='text-align:center;'>
                    <a href='https://docs.google.com/spreadsheets/d/1BPwecYI9zenjxQniEGgkh7CqBOSjOATi3R-2IRot4ow/edit?gid=890601984#gid=890601984' 
                       target='_blank' style='text-decoration: none;'>
                       <div class='planilha-button'>
                           <div class='planilha-title'>📋 PLANILHA DE CARTA DE IMÓVEIS</div>
                           <div class='planilha-desc'>Acesso à planilha completa de imóveis disponíveis</div>
                       </div>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col_plan2:
            st.markdown(
                """
                <div style='text-align:center;'>
                    <a href='https://docs.google.com/spreadsheets/d/1T4FRm4KUVQjD4aSg3Hn_FI6E0h_m8KbfaPGnlviXydI/edit?usp=sharing' 
                       target='_blank' style='text-decoration: none;'>
                       <div class='planilha-button'>
                           <div class='planilha-title'>💰 GESTÃO ORÇAMENTÁRIA</div>
                           <div class='planilha-desc'>Controle financeiro - contas a pagar e receber</div>
                       </div>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

    # PÁGINAS DOS MÓDULOS
    else:
        # SEM CONTAINER - deixe os scripts cuidarem disso
        col_back, col_title = st.columns([1, 4])
        with col_back:
            if st.button("⬅️ VOLTAR", use_container_width=True):
                mudar_pagina("inicial")
        with col_title:
            st.markdown(f"<h2 style='color: white !important;'>📄 {st.session_state.pagina.upper().replace('_', ' ')}</h2>", unsafe_allow_html=True)
        
        st.markdown("---")

        # CHAMADA DOS SCRIPTS SEM CONFLITO
        try:
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
        except Exception as e:
            st.error(f"Erro ao carregar o módulo: {e}")
            if st.button("🔄 Tentar Novamente"):
                st.rerun()

# ----------------- Execução -----------------
if not st.session_state.logged_in:
    login()
else:
    dashboard()