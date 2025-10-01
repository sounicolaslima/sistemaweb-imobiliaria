import streamlit as st
from docxtpl import DocxTemplate
import os, json
from datetime import datetime
from io import BytesIO  # usado para gerar arquivo em memória

# ---------------- Configuração JSON ----------------
ARQUIVO_DADOS = "dados.json"

def carregar_todos():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_todos(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

dados_todos = carregar_todos()

# ---------------- Geração do contrato ----------------
def gerar_contrato(dados):
    try:
        if not os.path.exists("contrato_administracao.docx"):
            st.error("Arquivo 'contrato_administracao.docx' não encontrado na pasta!")
            return

        doc = DocxTemplate("contrato_administracao.docx")
        cpf = dados.get("CPFLocatario")
        if not cpf:
            st.error("CPF do Locatário é obrigatório!")
            return

        # Características do imóvel
        caracteristicas = [c.strip() for c in dados.get("caracteristicasImovel", []) if c.strip()]
        dados["caracteristicasImovel"] = ", ".join(caracteristicas)

        # Atualiza JSON
        dados_todos[cpf] = dados
        salvar_todos(dados_todos)

        # Renderiza contrato
        doc.render(dados)

        # Gera arquivo em memória
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        # Nome do arquivo
        nome_arquivo = f"Contrato_{cpf}_{datetime.today().strftime('%Y%m%d')}.docx"

        # Botão de download direto
        st.success("✅ Contrato gerado com sucesso!")
        st.download_button(
            "📥 Baixar Contrato",
            buffer,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key="download_contrato_admin"
        )

    except Exception as e:
        st.error(f"Erro ao gerar contrato: {e}")

# ---------------- Carregar por CPF ----------------
def carregar_por_cpf(cpf):
    if not cpf:
        st.error("Digite o CPF do Locatário para buscar.")
        return {}
    if cpf in dados_todos:
        st.success(f"Dados carregados para o CPF {cpf}.")
        return dados_todos[cpf]
    else:
        st.info(f"Nenhum dado encontrado para o CPF {cpf}.")
        return {}

# ---------------- Função app ----------------
def app():
    st.title("CONTRATO DE ADMINISTRAÇÃO")
    dados_ficha = {}

    # CPF do Locatário
    col1, col2 = st.columns([2,1])
    with col1:
        cpf_input = st.text_input("CPF do Locatário", key="cpf_admin")
        dados_ficha["CPFLocatario"] = cpf_input
    with col2:
        if st.button("Carregar por CPF", key="btn_carregar_admin"):
            dados_ficha.update(carregar_por_cpf(cpf_input))

    # Função para criar campos com colunas
    def criar_campos(campos, dados, n_col=2, prefix=""):
        res = {}
        cols = st.columns(n_col)
        col_index = 0
        for campo, label in campos:
            valor = dados.get(campo, "")
            res[campo] = cols[col_index].text_input(label, value=valor, key=f"{prefix}_{campo}")
            col_index = (col_index + 1) % n_col
        return res

    # ---------------- Proprietário ----------------
    st.subheader("Dados do Proprietário")
    campos_proprietario = [
        ("nomeProprietario","Nome"),("RGProprietario","RG"),("CPFProprietario","CPF"),
        ("profissaoProprietario","Profissão"),("estadoCivil","Estado Civil"),
        ("enderecoProprietario","Endereço"),("celProprietario","Celular"),("emailProprietario","E-mail")
    ]
    dados_ficha.update(criar_campos(campos_proprietario, dados_ficha, n_col=2, prefix="prop"))

    # ---------------- Dados Bancários ----------------
    st.subheader("Dados Bancários")
    campos_banco = [
        ("banco","Banco"),("agencia","Agência"),("conta","Conta Corrente"),("declaracaoImposto","Declaração IR")
    ]
    dados_ficha.update(criar_campos(campos_banco, dados_ficha, n_col=2, prefix="banco"))

    # ---------------- Imóvel ----------------
    st.subheader("Imóvel Objeto da Administração")
    dados_ficha.update({"enderecoImovel": st.text_input("Endereço", value=dados_ficha.get("enderecoImovel",""), key="endereco_imovel")})

    # ---------------- Características do imóvel ----------------
    st.subheader("Características do Imóvel")
    caracteristicas = dados_ficha.get("caracteristicasImovel", [])
    carac_input = st.text_area("Digite cada característica separada por vírgula", value=", ".join(caracteristicas), key="carac_imovel")
    dados_ficha["caracteristicasImovel"] = [c.strip() for c in carac_input.split(",")]

    # ---------------- Serviços e Tributos ----------------
    st.subheader("Serviços e Tributos")
    campos_servicos = [
        ("matriculaCopasa","COPASA Matrícula"),("hidrometro","Nº Hidrômetro"),
        ("cemigInstal","CEMIG Instalação"),("numeroMedidor","Nº Medidor"),
        ("IPTUImovel","IPTU Imóvel"),("InscricaoIPTU","Inscrição Cadastral")
    ]
    dados_ficha.update(criar_campos(campos_servicos, dados_ficha, n_col=2, prefix="serv"))

    # ---------------- Contrato ----------------
    st.subheader("Dados do Contrato")
    campos_contrato = [
        ("dataAluguel","Dia do Pagamento"),("dataInicioContrato","Data Início"),
        ("valorAluguel","Valor do Aluguel"),("dataContrato","Data do Contrato")
    ]
    dados_ficha.update(criar_campos(campos_contrato, dados_ficha, n_col=2, prefix="contrato"))

    # ---------------- Testemunhas ----------------
    st.subheader("Testemunhas")
    campos_testemunhas = [
        ("nomeTestemunha1","Nome Testemunha 1"),("CPFTestemunha1","CPF Testemunha 1"),
        ("nomeTestemunha2","Nome Testemunha 2"),("CPFTestemunha2","CPF Testemunha 2")
    ]
    dados_ficha.update(criar_campos(campos_testemunhas, dados_ficha, n_col=2, prefix="test"))

    # ---------------- Botão gerar contrato ----------------
    if st.button("Gerar Contrato", key="btn_gerar_admin"):
        gerar_contrato(dados_ficha)
