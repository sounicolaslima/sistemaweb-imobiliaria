# fichaCadastral.py
import streamlit as st
from docxtpl import DocxTemplate, RichText
import os, json
from io import BytesIO

def app():
    # ----------------- Caminho relativo do arquivo Word -----------------
    base_dir = os.path.dirname(__file__)  # pasta onde está o script
    CAMINHO_DOCX = os.path.join(base_dir, "fichaCadastral.docx")  # template
    ARQUIVO_DADOS = os.path.join(base_dir, "dados.json")  # JSON de dados

    # ----------------- Funções JSON -----------------
    def carregar_todos():
        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, ValueError):
                with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                    json.dump({}, f)
                return {}
        else:
            with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                json.dump({}, f)
            return {}

    def salvar_todos(dados):
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    dados_todos = carregar_todos()
    st.title("FICHA CADASTRAL")

    # ----------------- Identificação Locatário -----------------
    st.subheader("Identificação do Locatário")
    cpf = st.text_input("CPF do Locatário")
    if st.button("Carregar por CPF"):
        if cpf in dados_todos:
            dados = dados_todos[cpf]
            st.session_state.update(dados)
            st.success(f"Dados carregados para CPF {cpf}")
        else:
            st.info(f"Nenhum dado encontrado para CPF {cpf}")

    # ----------------- Dados do Locatário -----------------
    st.subheader("Dados do Locatário")
    nomeLocatario = st.text_input("Nome")
    RG = st.text_input("RG")
    endereco = st.text_input("Endereço")
    valorLocacao = st.text_input("Valor Locação")
    dataEntrada = st.text_input("Data Entrada")
    dataVenc = st.text_input("Vencimento")
    celular = st.text_input("Celular")
    email = st.text_input("E-mail")

    # ----------------- Fiadores -----------------
    st.subheader("Fiadores")
    if "fiadores" not in st.session_state:
        st.session_state.fiadores = []
    if st.button("Adicionar Fiador"):
        st.session_state.fiadores.append({
            "nome": "", "rg": "", "cpf": "", "end": "", "cel": "", "email": ""
        })
    for idx, f in enumerate(st.session_state.fiadores):
        st.markdown(f"**Fiador {idx+1}**")
        f["nome"] = st.text_input(f"Nome Fiador {idx+1}", f.get("nome", ""), key=f"nome{idx}")
        f["rg"] = st.text_input(f"RG Fiador {idx+1}", f.get("rg", ""), key=f"rg{idx}")
        f["cpf"] = st.text_input(f"CPF Fiador {idx+1}", f.get("cpf", ""), key=f"cpf{idx}")
        f["end"] = st.text_input(f"Endereço Fiador {idx+1}", f.get("end", ""), key=f"end{idx}")
        f["cel"] = st.text_input(f"Celular Fiador {idx+1}", f.get("cel", ""), key=f"cel{idx}")
        f["email"] = st.text_input(f"E-mail Fiador {idx+1}", f.get("email", ""), key=f"email{idx}")

    # ----------------- Proprietário -----------------
    st.subheader("Dados do Proprietário")
    nomeProprietario = st.text_input("Nome Proprietário")
    RGProprietario = st.text_input("RG Proprietário")
    CPFProprietario = st.text_input("CPF Proprietário")
    enderecoProprietario = st.text_input("Endereço Proprietário")
    celProprietario = st.text_input("Celular Proprietário")
    emailProprietario = st.text_input("E-mail Proprietário")

    # ----------------- Dados Bancários -----------------
    st.subheader("Dados Bancários")
    banco = st.text_input("Banco")
    agencia = st.text_input("Agência")
    conta = st.text_input("Conta Corrente")
    declaracaoImposto = st.text_input("Declaração IR")

    # ----------------- Dados do Imóvel -----------------
    st.subheader("Dados do Imóvel")
    enderecoImovel = st.text_input("Endereço do Imóvel")

    # ----------------- Características -----------------
    st.subheader("Características do Imóvel")
    if "caracteristicas" not in st.session_state:
        st.session_state.caracteristicas = []
    if st.button("Adicionar Característica"):
        st.session_state.caracteristicas.append("")
    for i, carac in enumerate(st.session_state.caracteristicas):
        st.session_state.caracteristicas[i] = st.text_input(f"Característica {i+1}", carac, key=f"carac{i}")

    # ----------------- Serviços e Tributos -----------------
    st.subheader("Serviços e Tributos")
    CemigInstal = st.text_input("CEMIG Instalação")
    matriculaCopasa = st.text_input("COPASA Matrícula")
    IPTU = st.text_input("IPTU")

    # ----------------- Função gerar ficha -----------------
    def gerar_ficha_streamlit():
        if not os.path.exists(CAMINHO_DOCX):
            st.error(f"Arquivo {CAMINHO_DOCX} não encontrado.")
            return None

        doc = DocxTemplate(CAMINHO_DOCX)
        dados = {
            "cpf": cpf,
            "nomeLocatario": nomeLocatario,
            "RG": RG,
            "endereco": endereco,
            "valorLocacao": valorLocacao,
            "dataEntrada": dataEntrada,
            "dataVenc": dataVenc,
            "celular": celular,
            "email": email,
            "nomeProprietario": nomeProprietario,
            "RGProprietario": RGProprietario,
            "CPFProprietario": CPFProprietario,
            "enderecoProprietario": enderecoProprietario,
            "celProprietario": celProprietario,
            "emailProprietario": emailProprietario,
            "banco": banco,
            "agencia": agencia,
            "conta": conta,
            "declaracaoImposto": declaracaoImposto,
            "enderecoImovel": enderecoImovel,
            "CemigInstal": CemigInstal,
            "matriculaCopasa": matriculaCopasa,
            "IPTU": IPTU
        }

        # Características
        caracteristicas = [c for c in st.session_state.caracteristicas if c.strip()]
        dados["caracteristicaImovel"] = ", ".join(caracteristicas)

        # Fiadores
        lista_fiadores_json = []
        for f in st.session_state.fiadores:
            if f["nome"] or f["rg"] or f["cpf"]:
                bloco = f"Nome: {f['nome']}\nRG: {f['rg']}\nCPF: {f['cpf']}\nEndereço: {f['end']}\nCelular: {f['cel']}\nE-mail: {f['email']}"
                lista_fiadores_json.append(bloco)

        dados_todos[cpf] = {**dados, "fiadores": lista_fiadores_json}
        salvar_todos(dados_todos)

        fiadores_richtext = []
        for f in lista_fiadores_json:
            linhas = f.split("\n")
            rt = RichText()
            for linha in linhas:
                if ":" in linha:
                    chave, valor = linha.split(":", 1)
                    rt.add(chave + ": ", bold=True)
                    rt.add(valor.strip() + "\n")
            fiadores_richtext.append(rt)

        render_data = {**dados, "fiadores": fiadores_richtext}
        doc.render(render_data)

        # Salvar apenas em memória
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer

    # ----------------- Botão gerar/download -----------------
    if st.button("Gerar Ficha e Baixar"):
        arquivo = gerar_ficha_streamlit()
        if arquivo:
            nome_locatario_clean = nomeLocatario.replace(" ", "_") if nomeLocatario else "SemNome"
            data_contrato_clean = dataEntrada.replace("/", "-") if dataEntrada else "SemData"
            nome_arquivo = f"Ficha_{nome_locatario_clean}_{data_contrato_clean}.docx"

            st.download_button(
            label="📥 Clique aqui para baixar a ficha",
            data=arquivo,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            st.success("Ficha gerada com sucesso!")

