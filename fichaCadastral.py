# fichaCadastral.py
import streamlit as st
from docxtpl import DocxTemplate, RichText
import os, json
from io import BytesIO

def app():
    from theme import apply_theme
    apply_theme()
    
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
    
    # ----------------- Configuração da Página -----------------
    st.set_page_config(page_title="Ficha Cadastral", layout="centered")
    
    # CSS ORIGINAL mantido
    st.markdown("""
        <style>
            .main-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .section-header {
                text-align: center;
                margin: 25px 0 15px 0;
                padding: 12px;
                background-color: #f0f2f6;
                border-radius: 8px;
                border-left: 4px solid #4CAF50;
            }
            .stButton button {
                width: 100%;
            }
            .warning-box {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 15px;
                margin: 15px 0;
            }
            .subheader {
                margin: 20px 0 10px 0;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
                border-left: 3px solid #2196F3;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # CORREÇÃO: Botão voltar no topo + compatibilidade
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "inicial"

    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ VOLTAR", use_container_width=True, key="voltar_ficha_cadastral"):
            st.session_state.pagina = "inicial"
            st.rerun()
    with col_title:
        st.title("📋 FICHA CADASTRAL")

    # ----------------- Identificação Locatário -----------------
    st.markdown('<div class="section-header"><h3>BUSCAR DADOS EXISTENTES</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        cpf = st.text_input("CPF do Locatário", placeholder="000.000.000-00")
    with col2:
        if st.button("🔍 Carregar", use_container_width=True, key="carregar_ficha_cadastral"):
            if cpf in dados_todos:
                dados = dados_todos[cpf]
                st.session_state.update(dados)
                st.success(f"Dados carregados para CPF {cpf}")
            else:
                st.info(f"Nenhum dado encontrado para CPF {cpf}")

    # ----------------- Dados do Locatário -----------------
    st.markdown('<div class="section-header"><h3>DADOS DO LOCATÁRIO</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        nomeLocatario = st.text_input("Nome", value=st.session_state.get("nomeLocatario", ""), placeholder="Nome completo do locatário")
        RG = st.text_input("RG", value=st.session_state.get("RG", ""), placeholder="00.000.000-0")
        endereco = st.text_input("Endereço", value=st.session_state.get("endereco", ""), placeholder="Endereço completo")
        valorLocacao = st.text_input("Valor Locação", value=st.session_state.get("valorLocacao", ""), placeholder="R$ 0,00")
    
    with col2:
        dataEntrada = st.text_input("Data Entrada", value=st.session_state.get("dataEntrada", ""), placeholder="DD/MM/AAAA")
        dataVenc = st.text_input("Vencimento", value=st.session_state.get("dataVenc", ""), placeholder="DD/MM")
        celular = st.text_input("Celular", value=st.session_state.get("celular", ""), placeholder="(00) 00000-0000")
        email = st.text_input("E-mail", value=st.session_state.get("email", ""), placeholder="email@exemplo.com")

    # ----------------- Fiadores -----------------
    st.markdown('<div class="section-header"><h3>FIADORES</h3></div>', unsafe_allow_html=True)
    
    if "fiadores" not in st.session_state:
        st.session_state.fiadores = []
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Adicionar Fiador", use_container_width=True, key="adicionar_fiador_ficha"):
            st.session_state.fiadores.append({
                "nome": "", "rg": "", "cpf": "", "end": "", "cel": "", "email": ""
            })
            st.rerun()

    for idx, f in enumerate(st.session_state.fiadores):
        st.markdown(f"**Fiador {idx+1}**")
        col1, col2 = st.columns(2)
        with col1:
            f["nome"] = st.text_input(f"Nome Fiador {idx+1}", f.get("nome", ""), key=f"nome{idx}", placeholder="Nome completo")
            f["rg"] = st.text_input(f"RG Fiador {idx+1}", f.get("rg", ""), key=f"rg{idx}", placeholder="00.000.000-0")
            f["cpf"] = st.text_input(f"CPF Fiador {idx+1}", f.get("cpf", ""), key=f"cpf{idx}", placeholder="000.000.000-00")
        with col2:
            f["end"] = st.text_input(f"Endereço Fiador {idx+1}", f.get("end", ""), key=f"end{idx}", placeholder="Endereço completo")
            f["cel"] = st.text_input(f"Celular Fiador {idx+1}", f.get("cel", ""), key=f"cel{idx}", placeholder="(00) 00000-0000")
            f["email"] = st.text_input(f"E-mail Fiador {idx+1}", f.get("email", ""), key=f"email{idx}", placeholder="email@exemplo.com")

    # ----------------- Proprietário -----------------
    st.markdown('<div class="section-header"><h3>DADOS DO PROPRIETÁRIO</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        nomeProprietario = st.text_input("Nome Proprietário", value=st.session_state.get("nomeProprietario", ""), placeholder="Nome completo do proprietário")
        RGProprietario = st.text_input("RG Proprietário", value=st.session_state.get("RGProprietario", ""), placeholder="00000000")
        CPFProprietario = st.text_input("CPF Proprietário", value=st.session_state.get("CPFProprietario", ""), placeholder="000.000.000-00")
    
    with col2:
        enderecoProprietario = st.text_input("Endereço Proprietário", value=st.session_state.get("enderecoProprietario", ""), placeholder="Endereço completo")
        celProprietario = st.text_input("Celular Proprietário", value=st.session_state.get("celProprietario", ""), placeholder="(00) 00000-0000")
        emailProprietario = st.text_input("E-mail Proprietário", value=st.session_state.get("emailProprietario", ""), placeholder="email@exemplo.com")

    # ----------------- Dados Bancários -----------------
    st.markdown('<div class="section-header"><h3>DADOS BANCÁRIOS</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        banco = st.text_input("Banco", value=st.session_state.get("banco", ""), placeholder="Nome do banco")
        agencia = st.text_input("Agência", value=st.session_state.get("agencia", ""), placeholder="Número da agência")
    
    with col2:
        conta = st.text_input("Conta Corrente", value=st.session_state.get("conta", ""), placeholder="Número da conta")
        declaracaoImposto = st.text_input("Declaração IR", value=st.session_state.get("declaracaoImposto", ""), placeholder="Declaração de imposto de renda")

    # ----------------- Dados do Imóvel -----------------
    st.markdown('<div class="section-header"><h3>DADOS DO IMÓVEL</h3></div>', unsafe_allow_html=True)
    
    enderecoImovel = st.text_input("Endereço do Imóvel", value=st.session_state.get("enderecoImovel", ""), placeholder="Endereço completo do imóvel")

    # ----------------- Características -----------------
    st.markdown('<div class="section-header"><h3>CARACTERÍSTICAS DO IMÓVEL</h3></div>', unsafe_allow_html=True)
    
    if "caracteristicas" not in st.session_state:
        st.session_state.caracteristicas = []
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Adicionar Característica", use_container_width=True, key="adicionar_caracteristica_ficha"):
            st.session_state.caracteristicas.append("")
            st.rerun()

    for i, carac in enumerate(st.session_state.caracteristicas):
        st.session_state.caracteristicas[i] = st.text_input(
            f"Característica {i+1}", 
            carac, 
            key=f"carac{i}",
            placeholder="Ex: 3 quartos, 2 banheiros, garagem, etc."
        )

    # ----------------- Serviços e Tributos -----------------
    st.markdown('<div class="section-header"><h3>SERVIÇOS E TRIBUTOS</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        CemigInstal = st.text_input("CEMIG Instalação", value=st.session_state.get("CemigInstal", ""), placeholder="Número da instalação")
        matriculaCopasa = st.text_input("COPASA Matrícula", value=st.session_state.get("matriculaCopasa", ""), placeholder="Número da matrícula")
    
    with col2:
        IPTU = st.text_input("IPTU", value=st.session_state.get("IPTU", ""), placeholder="Valor do IPTU")

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
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 GERAR FICHA CADASTRAL", use_container_width=True, type="primary"):
            arquivo = gerar_ficha_streamlit()
            if arquivo:
                nome_locatario_clean = nomeLocatario.replace(" ", "_") if nomeLocatario else "SemNome"
                data_contrato_clean = dataEntrada.replace("/", "-") if dataEntrada else "SemData"
                nome_arquivo = f"Ficha_{nome_locatario_clean}_{data_contrato_clean}.docx"

                st.success("✅ Ficha gerada com sucesso!")
                st.download_button(
                    label="📥 BAIXAR FICHA CADASTRAL",
                    data=arquivo,
                    file_name=nome_arquivo,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
    
    # CORREÇÃO: REMOVIDO o fechamento do container
    # st.markdown('</div>', unsafe_allow_html=True) 
    
if __name__ == "__main__":
    app()
    