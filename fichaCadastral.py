import streamlit as st
from docxtpl import DocxTemplate
import os
from datetime import datetime

TEMPLATE = "fichaCadastral.docx"

def app():
    st.title("📄 Gerador de Ficha Cadastral")

    # ---------------- Locatário ----------------
    st.header("Dados do Locatário")
    cpf = st.text_input("CPF do Locatário", key="cpf_locatario_ficha")
    nomeLocatario = st.text_input("Nome do Locatário", key="nome_locatario_ficha")
    RG = st.text_input("RG do Locatário", key="rg_locatario_ficha")
    endereco = st.text_input("Endereço do Locatário", key="endereco_locatario_ficha")
    valorLocacao = st.text_input("Valor da Locação", key="valor_locacao_ficha")
    dataEntrada = st.date_input("Data de Entrada", key="data_entrada_ficha")
    dataVenc = st.text_input("Dia de vencimento", key="data_venc_ficha")
    celular = st.text_input("Celular", key="celular_locatario_ficha")
    email = st.text_input("E-mail", key="email_locatario_ficha")

    # ---------------- Fiadores ----------------
    st.header("Fiadores")
    fiadores = []
    num_fiadores = st.number_input("Quantos fiadores deseja incluir?", min_value=0, max_value=5, value=1, key="num_fiadores_ficha")

    for i in range(num_fiadores):
        st.subheader(f"Fiador {i+1}")
        nome = st.text_input(f"Nome do Fiador {i+1}", key=f"nome_fiador_{i}_ficha")
        rg = st.text_input(f"RG do Fiador {i+1}", key=f"rg_fiador_{i}_ficha")
        cpf_f = st.text_input(f"CPF do Fiador {i+1}", key=f"cpf_fiador_{i}_ficha")
        end = st.text_input(f"Endereço do Fiador {i+1}", key=f"endereco_fiador_{i}_ficha")
        cel = st.text_input(f"Celular do Fiador {i+1}", key=f"cel_fiador_{i}_ficha")
        email_f = st.text_input(f"E-mail do Fiador {i+1}", key=f"email_fiador_{i}_ficha")
        if nome or rg or cpf_f:
            fiadores.append({
                "nome": nome, "rg": rg, "cpf": cpf_f,
                "end": end, "cel": cel, "email": email_f
            })

    # ---------------- Proprietário ----------------
    st.header("Proprietário")
    nomeProprietario = st.text_input("Nome do Proprietário", key="nome_proprietario_ficha")
    RGProprietario = st.text_input("RG do Proprietário", key="rg_proprietario_ficha")
    CPFProprietario = st.text_input("CPF do Proprietário", key="cpf_proprietario_ficha")
    enderecoProprietario = st.text_input("Endereço do Proprietário", key="endereco_proprietario_ficha")
    celProprietario = st.text_input("Celular do Proprietário", key="cel_proprietario_ficha")
    emailProprietario = st.text_input("E-mail do Proprietário", key="email_proprietario_ficha")

    # ---------------- Botão ----------------
    if st.button("Gerar Ficha Cadastral", key="gerar_ficha_ficha"):
        if not os.path.exists(TEMPLATE):
            st.error("⚠️ Modelo 'fichaCadastral.docx' não encontrado na pasta!")
        elif not cpf or not nomeLocatario:
            st.error("⚠️ CPF e Nome do Locatário são obrigatórios!")
        else:
            doc = DocxTemplate(TEMPLATE)
            dados = {
                "cpf": cpf,
                "nomeLocatario": nomeLocatario,
                "RG": RG,
                "endereco": endereco,
                "valorLocacao": valorLocacao,
                "dataEntrada": dataEntrada.strftime("%d/%m/%Y"),
                "dataVenc": dataVenc,
                "celular": celular,
                "email": email,
                "nomeProprietario": nomeProprietario,
                "RGProprietario": RGProprietario,
                "CPFProprietario": CPFProprietario,
                "enderecoProprietario": enderecoProprietario,
                "celProprietario": celProprietario,
                "emailProprietario": emailProprietario,
                "fiadores": fiadores
            }

            # Gera o documento
            doc.render(dados)
            pasta_saida = "FichasGeradas"
            os.makedirs(pasta_saida, exist_ok=True)
            nome_arquivo = f"Ficha_{nomeLocatario}_{datetime.today().strftime('%Y%m%d')}.docx"
            caminho = os.path.join(pasta_saida, nome_arquivo)
            doc.save(caminho)

            # Botão de download
            with open(caminho, "rb") as f:
                st.success("✅ Ficha gerada com sucesso!")
                st.download_button("📥 Baixar Ficha Cadastral", f, file_name=nome_arquivo, key="download_ficha_ficha")
