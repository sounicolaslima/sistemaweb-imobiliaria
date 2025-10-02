import streamlit as st
from docxtpl import DocxTemplate, RichText
import os, json
from datetime import datetime
from io import BytesIO

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

        # Atualiza JSON (incluindo o novo campo mesDeDesocupacao)
        dados_todos[cpf] = {**dados, "fiadores": lista_fiadores_json}
        salvar_todos(dados_todos)

        # Renderiza documento (incluindo o novo campo)
        render_data = {**dados, "fiadores": fiadores_richtext}
        doc.render(render_data)

        # 🔹 Gerar apenas em memória
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        nome_locatario = dados.get("nomeLocatario","SemNome").replace(" ", "_")
        data_contrato = dados.get("dataContrato","SemData").replace("/", "-")
        nome_arquivo = f"Contrato_{nome_locatario}_{data_contrato}.docx"

        # Botão de download
        st.success("✅ Contrato gerado com sucesso!")
        st.download_button(
        label="📥 Baixar Contrato",
        data=buffer,
        file_name=nome_arquivo,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        key="download_contrato_locacao"
        )

    except Exception as e:
        st.error(f"Erro ao gerar contrato: {e}")

# ---------------- Função app ----------------
def app():
    st.set_page_config(page_title="Gerador de Contrato de Locação", layout="centered")
    
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
    
    st.title("📄 CONTRATO DE LOCAÇÃO")
    dados_ficha = {}

    # ----------------- CPF e Busca -----------------
    st.markdown('<div class="section-header"><h3>BUSCAR DADOS EXISTENTES</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        cpf_input = st.text_input("CPF do Locatário", key="cpf_locatario", placeholder="000.000.000-00")
        dados_ficha["cpf"] = cpf_input
    
    with col2:
        if st.button("🔍 Carregar", use_container_width=True):
            dados_ficha.update(carregar_por_cpf(cpf_input))

    # Função para criar campos
    def criar_campos(campos, dados, prefix=""):
        res = {}
        for campo, label in campos:
            valor = dados.get(campo, "")
            res[campo] = st.text_input(label, value=valor, key=f"{prefix}_{campo}")
        return res

    # ---------------- Dados do Locatário ----------------
    st.markdown('<div class="section-header"><h3>DADOS DO LOCATÁRIO</h3></div>', unsafe_allow_html=True)
    
    campos_locatario = [
        ("nomeLocatario","Nome"),("RG","RG"),("endereco","Endereço"),
        ("valorLocacao","Valor da Locação"),("dataVenc","Vencimento"),
        ("dataEntrada","Data de Entrada"),("celular","Celular"),("email","E-mail")
    ]
    
    # Organizando os campos em colunas
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["nomeLocatario"] = st.text_input("Nome", value=dados_ficha.get("nomeLocatario", ""), placeholder="Nome completo do locatário")
        dados_ficha["RG"] = st.text_input("RG", value=dados_ficha.get("RG", ""), placeholder="00.000.000-0")
        dados_ficha["email"] = st.text_input("E-mail", value=dados_ficha.get("email", ""), placeholder="email@exemplo.com")
        dados_ficha["dataEntrada"] = st.text_input("Data de Entrada", value=dados_ficha.get("dataEntrada", ""), placeholder="DD/MM/AAAA")
        
    
    with col2:
        dados_ficha["endereco"] = st.text_input("Endereço", value=dados_ficha.get("endereco", ""), placeholder="Endereço completo")
        dados_ficha["celular"] = st.text_input("Celular", value=dados_ficha.get("celular", ""), placeholder="(00) 00000-0000")
        dados_ficha["valorLocacao"] = st.text_input("Valor da Locação", value=dados_ficha.get("valorLocacao", ""), placeholder="R$ 0,00 (Valor por extenso)")
        dados_ficha["dataVenc"] = st.text_input("Vencimento", value=dados_ficha.get("dataVenc", ""), placeholder="DD/MM")
        
        
        

    # ---------------- Fiadores ----------------
    st.markdown('<div class="section-header"><h3>FIADORES</h3></div>', unsafe_allow_html=True)
    
    if "num_fiadores" not in st.session_state:
        st.session_state.num_fiadores = 1
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Adicionar Fiador", use_container_width=True):
            st.session_state.num_fiadores += 1
            st.rerun()

    fiadores = []
    for i in range(st.session_state.num_fiadores):
        st.markdown(f"**Fiador {i+1}**")
        col1, col2 = st.columns(2)
        fiador = {}
        with col1:
            fiador["nome"] = st.text_input(f"Nome Fiador {i+1}", value=dados_ficha.get(f"fiador{i}_nome", ""), key=f"fiador{i}_nome", placeholder="Nome completo")
            fiador["rg"] = st.text_input(f"RG Fiador {i+1}", value=dados_ficha.get(f"fiador{i}_rg", ""), key=f"fiador{i}_rg", placeholder="00.000.000-0")
            fiador["cpf"] = st.text_input(f"CPF Fiador {i+1}", value=dados_ficha.get(f"fiador{i}_cpf", ""), key=f"fiador{i}_cpf", placeholder="000.000.000-00")
        with col2:
            fiador["end"] = st.text_input(f"Endereço Fiador {i+1}", value=dados_ficha.get(f"fiador{i}_end", ""), key=f"fiador{i}_end", placeholder="Endereço completo")
            fiador["cel"] = st.text_input(f"Celular Fiador {i+1}", value=dados_ficha.get(f"fiador{i}_cel", ""), key=f"fiador{i}_cel", placeholder="(00) 00000-0000")
            fiador["email"] = st.text_input(f"E-mail Fiador {i+1}", value=dados_ficha.get(f"fiador{i}_email", ""), key=f"fiador{i}_email", placeholder="email@exemplo.com")
        fiadores.append(fiador)
    dados_ficha["fiadores"] = fiadores

    # ---------------- Dados do Proprietário ----------------
    st.markdown('<div class="section-header"><h3>DADOS DO PROPRIETÁRIO</h3></div>', unsafe_allow_html=True)
    
    campos_proprietario = [
        ("nomeProprietario","Nome"),("RGProprietario","RG"),("CPFProprietario","CPF"),
        ("enderecoProprietario","Endereço"),("celProprietario","Celular"),("emailProprietario","E-mail")
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["nomeProprietario"] = st.text_input("Nome Proprietário", value=dados_ficha.get("nomeProprietario", ""), key="prop_nomeProprietario", placeholder="Nome completo")
        dados_ficha["RGProprietario"] = st.text_input("RG Proprietário", value=dados_ficha.get("RGProprietario", ""), key="prop_RGProprietario", placeholder="0000000")
        dados_ficha["CPFProprietario"] = st.text_input("CPF Proprietário", value=dados_ficha.get("CPFProprietario", ""), key="prop_CPFProprietario", placeholder="000.000.000-00")
    
    with col2:
        dados_ficha["enderecoProprietario"] = st.text_input("Endereço Proprietário", value=dados_ficha.get("enderecoProprietario", ""), key="prop_enderecoProprietario", placeholder="Endereço completo")
        dados_ficha["celProprietario"] = st.text_input("Celular Proprietário", value=dados_ficha.get("celProprietario", ""), key="prop_celProprietario", placeholder="(00) 00000-0000")
        dados_ficha["emailProprietario"] = st.text_input("E-mail Proprietário", value=dados_ficha.get("emailProprietario", ""), key="prop_emailProprietario", placeholder="email@exemplo.com")

    # ---------------- Dados do Imóvel ----------------
    st.markdown('<div class="section-header"><h3>DADOS DO IMÓVEL</h3></div>', unsafe_allow_html=True)
    
    campos_imovel = [
        ("tipoDoImovel","Tipo do Imóvel"),("EnderecoImovel","Endereço"),
        ("CEPImovel","CEP"),("CidadeImovel","Cidade")
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["tipoDoImovel"] = st.text_input("Tipo do Imóvel", value=dados_ficha.get("tipoDoImovel", ""), key="imovel_tipoDoImovel", placeholder="Casa, Apartamento, etc.")
        dados_ficha["EnderecoImovel"] = st.text_input("Endereço do Imóvel", value=dados_ficha.get("EnderecoImovel", ""), key="imovel_EnderecoImovel", placeholder="Endereço completo")
    
    with col2:
        dados_ficha["CEPImovel"] = st.text_input("CEP", value=dados_ficha.get("CEPImovel", ""), key="imovel_CEPImovel", placeholder="00000-000")
        dados_ficha["CidadeImovel"] = st.text_input("Cidade", value=dados_ficha.get("CidadeImovel", ""), key="imovel_CidadeImovel", placeholder="Cidade/UF")

    # ---------------- Características do Imóvel ----------------
    st.markdown('<div class="section-header"><h3>CARACTERÍSTICAS DO IMÓVEL</h3></div>', unsafe_allow_html=True)
    
    carac_input = st.text_area(
        "Digite as características separadas por vírgula",
        value=", ".join(dados_ficha.get("caracteristicasImovel", [])),
        key="carac_imovel",
        placeholder="Ex: 3 quartos, 2 banheiros, garagem, área de serviço, etc."
    )
    dados_ficha["caracteristicasImovel"] = [c.strip() for c in carac_input.split(",")]

    # ---------------- Serviços e Tributos ----------------
    st.markdown('<div class="section-header"><h3>SERVIÇOS E TRIBUTOS</h3></div>', unsafe_allow_html=True)
    
    campos_servicos = [
        ("matriculaCopasa","Matrícula Copasa"),("hidrometroCopasa","Hidrômetro Copasa"),
        ("CemigInstalacao","CEMIG Instalação"),("medidor","Nº Medidor"),
        ("IPTUImovel","IPTU"),("inscricaoIPTU","Inscrição IPTU")
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["matriculaCopasa"] = st.text_input("Matrícula Copasa", value=dados_ficha.get("matriculaCopasa", ""), key="serv_matriculaCopasa", placeholder="Número da matrícula")
        dados_ficha["CemigInstalacao"] = st.text_input("CEMIG Instalação", value=dados_ficha.get("CemigInstalacao", ""), key="serv_CemigInstalacao", placeholder="Número da instalação")
        dados_ficha["IPTUImovel"] = st.text_input("IPTU", value=dados_ficha.get("IPTUImovel", ""), key="serv_IPTUImovel", placeholder="IPTU")
       
    
    with col2:
        dados_ficha["hidrometroCopasa"] = st.text_input("Hidrômetro Copasa", value=dados_ficha.get("hidrometroCopasa", ""), key="serv_hidrometroCopasa", placeholder="Número do hidrômetro")
        dados_ficha["medidor"] = st.text_input("Nº Medidor", value=dados_ficha.get("medidor", ""), key="serv_medidor", placeholder="Número do medidor")
        dados_ficha["inscricaoIPTU"] = st.text_input("Inscrição IPTU", value=dados_ficha.get("inscricaoIPTU", ""), key="serv_inscricaoIPTU", placeholder="Número de inscrição")

    # ---------------- Duração do Contrato ----------------
    st.markdown('<div class="section-header"><h3>DURAÇÃO DO CONTRATO</h3></div>', unsafe_allow_html=True)
    
    campos_duracao = [
        ("duracao","Duração"),("dataInicio","Data Início"),("dataTermino","Data Término"),
        ("ValorLocacaoMensal","Valor Mensal"), ("mesDeDesocupacao", "Mês de Desocupação"),("dataContrato","Data do Contrato")
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["duracao"] = st.text_input("Duração", value=dados_ficha.get("duracao", ""), key="duracao_duracao", placeholder="Ex: 12 meses")
        dados_ficha["dataInicio"] = st.text_input("Data Início", value=dados_ficha.get("dataInicio", ""), key="duracao_dataInicio", placeholder="DD/MM/AAAA")
        dados_ficha["dataTermino"] = st.text_input("Data Término", value=dados_ficha.get("dataTermino", ""), key="duracao_dataTermino", placeholder="DD/MM/AAAA")
    
    with col2:
        dados_ficha["ValorLocacaoMensal"] = st.text_input("Valor Mensal", value=dados_ficha.get("ValorLocacaoMensal", ""), key="duracao_ValorLocacaoMensal", placeholder=" 0,00 (valor por extenso)")
        dados_ficha["mesDeDesocupacao"] = st.text_input("Mês de Desocupação", value=dados_ficha.get("mesDeDesocupacao", ""), key="duracao_mesDeDesocupacao", placeholder="Ex: 12º(décimo segundo)")
        dados_ficha["dataContrato"] = st.text_input("Data do Contrato", value=dados_ficha.get("dataContrato", ""), key="duracao_dataContrato", placeholder="Ex:Dia, Mês de Ano")

    # ----------------- Botão Gerar Documento -----------------
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 GERAR CONTRATO DE LOCAÇÃO", use_container_width=True, type="primary"):
            gerar_contrato(dados_ficha)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Executar -----------------
if __name__ == "__main__":
    app()