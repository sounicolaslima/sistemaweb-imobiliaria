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
    from theme import apply_theme
    apply_theme()
    
    st.set_page_config(page_title="Gerador de Contrato de Administração", layout="centered")
    
    # CSS para centralizar e estilizar
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
    
    st.title("📋 CONTRATO DE ADMINISTRAÇÃO")
    dados_ficha = {}

    # ----------------- CPF e Busca -----------------
    st.markdown('<div class="section-header"><h3>BUSCAR DADOS EXISTENTES</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        cpf_input = st.text_input("CPF do Locatário", key="cpf_admin", placeholder="000.000.000-00")
        dados_ficha["CPFLocatario"] = cpf_input
    
    with col2:
        if st.button("🔍 Carregar", use_container_width=True, key="btn_carregar_admin"):
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
    st.markdown('<div class="section-header"><h3>DADOS DO PROPRIETÁRIO</h3></div>', unsafe_allow_html=True)
    
    campos_proprietario = [
        ("nomeProprietario","Nome"),("RGProprietario","RG"),("CPFProprietario","CPF"),
        ("profissaoProprietario","Profissão"),("estadoCivil","Estado Civil"),
        ("enderecoProprietario","Endereço"),("celProprietario","Celular"),("emailProprietario","E-mail")
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["nomeProprietario"] = st.text_input("Nome", value=dados_ficha.get("nomeProprietario", ""), key="prop_nomeProprietario", placeholder="Nome completo do proprietário")
        dados_ficha["RGProprietario"] = st.text_input("RG", value=dados_ficha.get("RGProprietario", ""), key="prop_RGProprietario", placeholder="0000000")
        dados_ficha["CPFProprietario"] = st.text_input("CPF", value=dados_ficha.get("CPFProprietario", ""), key="prop_CPFProprietario", placeholder="000.000.000-00")
        dados_ficha["profissaoProprietario"] = st.text_input("Profissão", value=dados_ficha.get("profissaoProprietario", ""), key="prop_profissaoProprietario", placeholder="Profissão do proprietário")
    
    with col2:
        dados_ficha["estadoCivil"] = st.text_input("Estado Civil", value=dados_ficha.get("estadoCivil", ""), key="prop_estadoCivil", placeholder="Solteiro, Casado, etc.")
        dados_ficha["enderecoProprietario"] = st.text_input("Endereço", value=dados_ficha.get("enderecoProprietario", ""), key="prop_enderecoProprietario", placeholder="Endereço completo")
        dados_ficha["celProprietario"] = st.text_input("Celular", value=dados_ficha.get("celProprietario", ""), key="prop_celProprietario", placeholder="(00) 00000-0000")
        dados_ficha["emailProprietario"] = st.text_input("E-mail", value=dados_ficha.get("emailProprietario", ""), key="prop_emailProprietario", placeholder="email@exemplo.com")

    # ---------------- Dados Bancários ----------------
    st.markdown('<div class="section-header"><h3>DADOS BANCÁRIOS</h3></div>', unsafe_allow_html=True)
    
    campos_banco = [
        ("banco","Banco"),("agencia","Agência"),("conta","Conta Corrente"),("declaracaoImposto","Declaração IR")
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["banco"] = st.text_input("Banco", value=dados_ficha.get("banco", ""), key="banco_banco", placeholder="Nome do banco")
        dados_ficha["agencia"] = st.text_input("Agência", value=dados_ficha.get("agencia", ""), key="banco_agencia", placeholder="Número da agência")
    
    with col2:
        dados_ficha["conta"] = st.text_input("Conta Corrente", value=dados_ficha.get("conta", ""), key="banco_conta", placeholder="Número da conta")
        dados_ficha["declaracaoImposto"] = st.text_input("Declaração IR", value=dados_ficha.get("declaracaoImposto", ""), key="banco_declaracaoImposto", placeholder="Declaração de imposto de renda")

    # ---------------- Imóvel ----------------
    st.markdown('<div class="section-header"><h3>IMÓVEL OBJETO DA ADMINISTRAÇÃO</h3></div>', unsafe_allow_html=True)
    
    dados_ficha["enderecoImovel"] = st.text_input(
        "Endereço do Imóvel", 
        value=dados_ficha.get("enderecoImovel", ""), 
        key="endereco_imovel",
        placeholder="Endereço completo do imóvel"
    )

    # ---------------- Características do imóvel ----------------
    st.markdown('<div class="section-header"><h3>CARACTERÍSTICAS DO IMÓVEL</h3></div>', unsafe_allow_html=True)
    
    caracteristicas = dados_ficha.get("caracteristicasImovel", [])
    carac_input = st.text_area(
        "Digite cada característica separada por vírgula", 
        value=", ".join(caracteristicas), 
        key="carac_imovel",
        placeholder="Ex: 3 quartos, 2 banheiros, garagem, área de serviço, piscina, etc."
    )
    dados_ficha["caracteristicasImovel"] = [c.strip() for c in carac_input.split(",")]

    # ---------------- Serviços e Tributos ----------------
    st.markdown('<div class="section-header"><h3>SERVIÇOS E TRIBUTOS</h3></div>', unsafe_allow_html=True)
    
    campos_servicos = [
        ("matriculaCopasa","COPASA Matrícula"),("hidrometro","Nº Hidrômetro"),
        ("cemigInstal","CEMIG Instalação"),("numeroMedidor","Nº Medidor"),
        ("IPTUImovel","IPTU Imóvel"),("InscricaoIPTU","Inscrição Cadastral")
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["matriculaCopasa"] = st.text_input("COPASA Matrícula", value=dados_ficha.get("matriculaCopasa", ""), key="serv_matriculaCopasa", placeholder="Número da matrícula")
        dados_ficha["cemigInstal"] = st.text_input("CEMIG Instalação", value=dados_ficha.get("cemigInstal", ""), key="serv_cemigInstal", placeholder="Número da instalação")
        dados_ficha["IPTUImovel"] = st.text_input("IPTU Imóvel", value=dados_ficha.get("IPTUImovel", ""), key="serv_IPTUImovel", placeholder="IPTU")

    with col2:
        dados_ficha["hidrometro"] = st.text_input("Nº Hidrômetro", value=dados_ficha.get("hidrometro", ""), key="serv_hidrometro", placeholder="Número do hidrômetro")
        dados_ficha["numeroMedidor"] = st.text_input("Nº Medidor", value=dados_ficha.get("numeroMedidor", ""), key="serv_numeroMedidor", placeholder="Número do medidor")
        dados_ficha["InscricaoIPTU"] = st.text_input("Inscrição Cadastral", value=dados_ficha.get("InscricaoIPTU", ""), key="serv_InscricaoIPTU", placeholder="Número de inscrição")

    # ---------------- Contrato ----------------
    st.markdown('<div class="section-header"><h3>DADOS DO CONTRATO</h3></div>', unsafe_allow_html=True)
    
    campos_contrato = [
        ("dataAluguel","Dia do Pagamento"),("dataInicioContrato","Data Início"),
        ("valorAluguel","Valor do Aluguel"),("dataContrato","Data do Contrato")
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["dataAluguel"] = st.text_input("Dia do Pagamento", value=dados_ficha.get("dataAluguel", ""), key="contrato_dataAluguel", placeholder="Ex: 05 (cinco)")
        dados_ficha["dataInicioContrato"] = st.text_input("Data Início", value=dados_ficha.get("dataInicioContrato", ""), key="contrato_dataInicioContrato", placeholder="DD/MM/AAAA")
    
    with col2:
        dados_ficha["valorAluguel"] = st.text_input("Valor do Aluguel", value=dados_ficha.get("valorAluguel", ""), key="contrato_valorAluguel", placeholder="R$ 0,00 (valor por extenso)")
        dados_ficha["dataContrato"] = st.text_input("Data do Contrato", value=dados_ficha.get("dataContrato", ""), key="contrato_dataContrato", placeholder="Dia, Mês de Ano")

    # ---------------- Testemunhas ----------------
    st.markdown('<div class="section-header"><h3>TESTEMUNHAS</h3></div>', unsafe_allow_html=True)
    
    campos_testemunhas = [
        ("nomeTestemunha1","Nome Testemunha 1"),("CPFTestemunha1","CPF Testemunha 1"),
        ("nomeTestemunha2","Nome Testemunha 2"),("CPFTestemunha2","CPF Testemunha 2")
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["nomeTestemunha1"] = st.text_input("Nome Testemunha 1", value=dados_ficha.get("nomeTestemunha1", ""), key="test_nomeTestemunha1", placeholder="Nome completo")
        dados_ficha["CPFTestemunha1"] = st.text_input("CPF Testemunha 1", value=dados_ficha.get("CPFTestemunha1", ""), key="test_CPFTestemunha1", placeholder="000.000.000-00")
    
    with col2:
        dados_ficha["nomeTestemunha2"] = st.text_input("Nome Testemunha 2", value=dados_ficha.get("nomeTestemunha2", ""), key="test_nomeTestemunha2", placeholder="Nome completo")
        dados_ficha["CPFTestemunha2"] = st.text_input("CPF Testemunha 2", value=dados_ficha.get("CPFTestemunha2", ""), key="test_CPFTestemunha2", placeholder="000.000.000-00")

    # ----------------- Botão Gerar Documento -----------------
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 GERAR CONTRATO DE ADMINISTRAÇÃO", use_container_width=True, type="primary", key="btn_gerar_admin"):
            gerar_contrato(dados_ficha)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Executar -----------------
if __name__ == "__main__":
    app()