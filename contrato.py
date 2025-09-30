import streamlit as st
from docxtpl import DocxTemplate, RichText
import os, json
from datetime import datetime

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

# ---------------- Funções ----------------
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

def gerar_contrato(dados):
    try:
        if not os.path.exists("contrato.docx"):
            st.error("Arquivo 'contrato.docx' não encontrado na pasta!")
            return

        doc = DocxTemplate("contrato.docx")
        cpf = dados.get("cpf")
        if not cpf:
            st.error("CPF do locatário é obrigatório!")
            return

        # Características do imóvel
        caracteristicas = [c.strip() for c in dados.get("caracteristicasImovel", []) if c.strip()]
        dados["caracteristicasImovel"] = ", ".join(caracteristicas)

        # Fiadores
        fiadores_richtext = []
        lista_fiadores_json = []
        for f in dados.get("fiadores", []):
            bloco = f"Nome: {f.get('nome','')}\nRG: {f.get('rg','')}\nCPF: {f.get('cpf','')}\nEndereço: {f.get('end','')}\nCelular: {f.get('cel','')}\nE-mail: {f.get('email','')}"
            lista_fiadores_json.append(bloco)
            linhas = bloco.split("\n")
            rt = RichText()
            for linha in linhas:
                if ":" in linha:
                    chave, valor = linha.split(":",1)
                    rt.add(chave+": ", bold=True)
                    rt.add(valor.strip()+"\n")
            fiadores_richtext.append(rt)

        # Atualiza JSON
        dados_todos[cpf] = {**dados, "fiadores": lista_fiadores_json}
        salvar_todos(dados_todos)

        # Renderiza documento
        render_data = {**dados, "fiadores": fiadores_richtext}
        doc.render(render_data)

        # Salva o arquivo
        pasta_saida = "contratos"
        os.makedirs(pasta_saida, exist_ok=True)
        nome_locatario = dados.get("nomeLocatario","SemNome").replace(" ", "_")
        data_contrato = dados.get("dataContrato","SemData").replace("/", "-")
        nome_arquivo = f"Contrato_{nome_locatario}_{data_contrato}.docx"
        caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
        doc.save(caminho_arquivo)

        # Botão de download
        with open(caminho_arquivo, "rb") as f:
            st.success("✅ Contrato gerado com sucesso!")
            st.download_button("📥 Baixar Contrato", f, file_name=nome_arquivo, key="download_contrato_locacao")

    except Exception as e:
        st.error(f"Erro ao gerar contrato: {e}")

# ---------------- Função app ----------------
def app():
    st.title("CONTRATO DE LOCAÇÃO")
    dados_ficha = {}

    # CPF do Locatário
    cpf_input = st.text_input("CPF do Locatário", key="cpf_locatario")
    dados_ficha["cpf"] = cpf_input
    if st.button("Carregar por CPF"):
        dados_ficha.update(carregar_por_cpf(cpf_input))

    # Função para criar campos
    def criar_campos(campos, dados, prefix=""):
        res = {}
        for campo, label in campos:
            valor = dados.get(campo, "")
            res[campo] = st.text_input(label, value=valor, key=f"{prefix}_{campo}")
        return res

    # ---------------- Dados do Locatário ----------------
    st.subheader("Dados do Locatário")
    campos_locatario = [
        ("nomeLocatario","Nome"),("RG","RG"),("endereco","Endereço"),
        ("valorLocacao","Valor da Locação"),("dataVenc","Vencimento"),
        ("dataEntrada","Data de Entrada"),("celular","Celular"),("email","E-mail")
    ]
    dados_ficha.update(criar_campos(campos_locatario, dados_ficha, prefix="loc"))

    # ---------------- Fiadores ----------------
    st.subheader("Fiadores")
    if "num_fiadores" not in st.session_state:
        st.session_state.num_fiadores = 1
    if st.button("➕ Adicionar Fiador"):
        st.session_state.num_fiadores += 1

    fiadores = []
    for i in range(st.session_state.num_fiadores):
        st.markdown(f"**Fiador {i+1}**")
        fiador = {}
        fiador["nome"] = st.text_input(f"Nome Fiador {i+1}", value="", key=f"fiador{i}_nome")
        fiador["rg"] = st.text_input(f"RG Fiador {i+1}", value="", key=f"fiador{i}_rg")
        fiador["cpf"] = st.text_input(f"CPF Fiador {i+1}", value="", key=f"fiador{i}_cpf")
        fiador["end"] = st.text_input(f"Endereço Fiador {i+1}", value="", key=f"fiador{i}_end")
        fiador["cel"] = st.text_input(f"Celular Fiador {i+1}", value="", key=f"fiador{i}_cel")
        fiador["email"] = st.text_input(f"E-mail Fiador {i+1}", value="", key=f"fiador{i}_email")
        fiadores.append(fiador)
    dados_ficha["fiadores"] = fiadores

    # ---------------- Dados do Proprietário ----------------
    st.subheader("Dados do Proprietário")
    campos_proprietario = [
        ("nomeProprietario","Nome"),("RGProprietario","RG"),("CPFProprietario","CPF"),
        ("enderecoProprietario","Endereço"),("celProprietario","Celular"),("emailProprietario","E-mail")
    ]
    dados_ficha.update(criar_campos(campos_proprietario, dados_ficha, prefix="prop"))

    # ---------------- Dados do Imóvel ----------------
    st.subheader("Dados do Imóvel")
    campos_imovel = [
        ("tipoDoImovel","Tipo do Imóvel"),("EnderecoImovel","Endereço"),
        ("CEPImovel","CEP"),("CidadeImovel","Cidade")
    ]
    dados_ficha.update(criar_campos(campos_imovel, dados_ficha, prefix="imovel"))

    # ---------------- Características do Imóvel ----------------
    st.subheader("Características do Imóvel")
    carac_input = st.text_area("Digite as características separadas por vírgula", value=", ".join(dados_ficha.get("caracteristicasImovel", [])), key="carac_imovel")
    dados_ficha["caracteristicasImovel"] = [c.strip() for c in carac_input.split(",")]

    # ---------------- Serviços e Tributos ----------------
    st.subheader("Serviços e Tributos")
    campos_servicos = [
        ("matriculaCopasa","Matrícula Copasa"),("hidrometroCopasa","Hidrômetro Copasa"),
        ("CemigInstalacao","CEMIG Instalação"),("medidor","Nº Medidor"),
        ("IPTUImovel","IPTU"),("inscricaoIPTU","Inscrição IPTU")
    ]
    dados_ficha.update(criar_campos(campos_servicos, dados_ficha, prefix="serv"))

    # ---------------- Duração do Contrato ----------------
    st.subheader("Duração do Contrato")
    campos_duracao = [
        ("duracao","Duração"),("dataInicio","Data Início"),("dataTermino","Data Término"),
        ("ValorLocacaoMensal","Valor Mensal"),("dataContrato","Data do Contrato")
    ]
    dados_ficha.update(criar_campos(campos_duracao, dados_ficha, prefix="duracao"))

    # ---------------- Botão gerar contrato ----------------
    if st.button("Gerar Contrato"):
        gerar_contrato(dados_ficha)
