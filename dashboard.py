import streamlit as st
from PIL import Image

# ----------------- Configuração da página -----------------
st.set_page_config(page_title="Dashboard Villares", layout="wide")

# ----------------- Estado da página -----------------
if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicial"

def mudar_pagina(pagina):
    st.session_state.pagina = pagina

# ----------------- Tela Inicial -----------------
if st.session_state.pagina == "inicial":
    # --- Logo e título ---
    col_logo, col_title = st.columns([1,4])
    with col_logo:
        logo = Image.open("villares.png")
        st.image(logo, width=480)  
    with col_title:
        st.markdown("<h1 style='margin-top:30px'>📂 Central de Geradores de Documentos</h1>", unsafe_allow_html=True)
        st.markdown("### Villares Imobiliária", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Escolha o gerador que deseja usar:")

    # --- Cartões clicáveis ---
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄\nGerar Ficha Cadastral", key="ficha_cadastral"):
            mudar_pagina("ficha_cadastral")
        if st.button("📝\nGerar Contrato Administrativo", key="contrato_admin"):
            mudar_pagina("contrato_administrativo")

    with col2:
        if st.button("📃\nGerar Contrato", key="contrato"):
            mudar_pagina("contrato")
        if st.button("🏠\nGerar Ficha de Captação", key="ficha_captacao"):
            mudar_pagina("ficha_captacao")

    with col3:
        if st.button("📋\nGerar Termo de Vistoria", key="termo_vistoria"):
            mudar_pagina("termo_vistoria")

    # --- Link para a planilha como botão estilizado ---
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align:center; margin-top:20px'>
            <a href='https://docs.google.com/spreadsheets/d/1BPwecYI9zenjxQniEGgkh7CqBOSjOATi3R-2IRot4ow/edit?gid=890601984#gid=890601984' target='_blank'
               style='background-color:#4CAF50; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; font-size:16px;'>
               Acessar Planilha de carta de imóveis
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------- Chamando scripts -----------------
else:
    st.button("⬅️ Voltar", on_click=lambda: mudar_pagina("inicial"))

    if st.session_state.pagina == "ficha_cadastral":
        import fichaCadastral
        fichaCadastral.app()  # cada script deve ter função app()

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
