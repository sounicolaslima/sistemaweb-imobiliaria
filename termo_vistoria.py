import streamlit as st
from docxtpl import DocxTemplate
import os
from datetime import datetime

# ---------------- Caminho do modelo ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DOCX = os.path.join(BASE_DIR, "vistoria.docx")

def gerar_vistoria(dados):
    try:
        if not os.path.exists(CAMINHO_DOCX):
            st.error(f"⚠️ Arquivo {CAMINHO_DOCX} não encontrado.")
            return

        doc = DocxTemplate(CAMINHO_DOCX)
        doc.render(dados)

        pasta_saida = "VistoriasGeradas"
        os.makedirs(pasta_saida, exist_ok=True)

        cpf = dados.get("cpfLocatario", "SemCPF").strip().replace(" ", "_")
        data_atual = datetime.today().strftime("%Y-%m-%d")
        nome_arquivo = f"Vistoria_{cpf}_{data_atual}.docx"

        caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
        doc.save(caminho_arquivo)

        st.success("✅ Termo de Vistoria gerado com sucesso!")
        with open(caminho_arquivo, "rb") as f:
            st.download_button("📥 Baixar Termo de Vistoria", f, file_name=nome_arquivo, key="download_vistoria")

    except Exception as e:
        st.error(f"Erro ao gerar vistoria: {e}")

def app():
    # CPF antes do título
    cpf = st.text_input("CPF do Locatário", key="cpf_locatario_vistoria")

    st.title("📋 Termo de Vistoria")

    # ---------------- Locatário ----------------
    st.header("Dados do Locatário")
    nomeLocatario = st.text_input("Nome do Locatário", key="nome_locatario_vistoria")
    rgLocatario = st.text_input("RG do Locatário", key="rg_locatario_vistoria")
    enderecoLocatario = st.text_input("Endereço do Locatário", key="endereco_locatario_vistoria")

    # ---------------- Proprietário ----------------
    st.header("Dados do Proprietário")
    nomeProprietario = st.text_input("Nome do Proprietário", key="nome_proprietario_vistoria")
    cpfProprietario = st.text_input("CPF do Proprietário", key="cpf_proprietario_vistoria")

    # ---------------- Imóvel ----------------
    st.header("Dados do Imóvel")
    enderecoImovel = st.text_input("Endereço do Imóvel", key="endereco_imovel_vistoria")
    cidadeImovel = st.text_input("Cidade do Imóvel", key="cidade_imovel_vistoria")
    ufImovel = st.text_input("UF", key="uf_imovel_vistoria")

    # ---------------- Observações ----------------
    st.header("Observações")
    observacoes = st.text_area("Observações sobre a vistoria", key="obs_vistoria")

    # ---------------- Botão ----------------
    if st.button("Gerar Termo de Vistoria", key="gerar_vistoria"):
        dados = {
            "cpfLocatario": cpf,
            "nomeLocatario": nomeLocatario,
            "rgLocatario": rgLocatario,
            "enderecoLocatario": enderecoLocatario,
            "nomeProprietario": nomeProprietario,
            "cpfProprietario": cpfProprietario,
            "enderecoImovel": enderecoImovel,
            "cidadeImovel": cidadeImovel,
            "ufImovel": ufImovel,
            "observacoes": observacoes
        }
        gerar_vistoria(dados)
