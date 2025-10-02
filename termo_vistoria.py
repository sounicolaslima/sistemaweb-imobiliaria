import streamlit as st
from docxtpl import DocxTemplate
import os, json
from datetime import datetime
from io import BytesIO
import warnings

# Suprimir warnings desnecessários
warnings.filterwarnings("ignore")

# ----------------- Configurações -----------------
ARQUIVO_DADOS = "dados_vistorias.json"

# Caminho correto para o template na pasta 'vistoria'
CAMINHO_TEMPLATE = "vistoria/vistoria_corrigido_dinamico.docx"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Inicializar session states
if "fiadores" not in st.session_state:
    st.session_state.fiadores = [{}]

if "comodos" not in st.session_state:
    st.session_state.comodos = [{
        "nome": "Sala", 
        "caracteristicas": [
            {"nome": "Piso", "estado": "Bom", "descricao": ""},
            {"nome": "Parede", "estado": "Bom", "descricao": ""},
            {"nome": "Tomada", "estado": "Bom", "descricao": ""}
        ]
    }]

dados_todos = carregar_dados()

# ----------------- Função Principal -----------------
def app():
    st.set_page_config(page_title="Gerador de Vistoria", layout="centered")
    
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
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.title("📋 GERADOR DE TERMO DE VISTORIA")
    
    # Verificação do template
    if not os.path.exists(CAMINHO_TEMPLATE):
        st.markdown(f"""
        <div class="warning-box">
            <h3>⚠️ Template Não Encontrado</h3>
            <p>O arquivo <strong>{CAMINHO_TEMPLATE}</strong> não foi encontrado.</p>
            <p><strong>Por favor verifique:</strong></p>
            <ol>
                <li>Se a pasta <strong>'vistoria'</strong> existe</li>
                <li>Se o arquivo <strong>'vistoria_corrigido_dinamico.docx'</strong> está dentro da pasta 'vistoria'</li>
                <li>O nome exato do arquivo (incluindo letras maiúsculas/minúsculas)</li>
            </ol>
            <p><strong>Diretório atual:</strong> {os.getcwd()}</p>
            <p><strong>Arquivos na pasta atual:</strong> {', '.join(os.listdir('.'))}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Verificar se a pasta vistoria existe e mostrar seu conteúdo
        if os.path.exists("vistoria"):
            st.info(f"📁 Conteúdo da pasta 'vistoria': {', '.join(os.listdir('vistoria'))}")
        else:
            st.error("❌ A pasta 'vistoria' não existe!")
        
        st.stop()

    else:
        st.success(f"✅ Template encontrado: {CAMINHO_TEMPLATE}")
    
    dados_ficha = {}

    # ----------------- CPF e Busca -----------------
    st.markdown('<div class="section-header"><h3>BUSCAR DADOS EXISTENTES</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        cpf_input = st.text_input("CPF do Locatário", key="cpf_vistoria", placeholder="000.000.000-00")
        dados_ficha["CPFLocatario"] = cpf_input
    
    with col2:
        if st.button("🔍 Carregar", use_container_width=True):
            if cpf_input and cpf_input in dados_todos:
                dados_ficha.update(dados_todos[cpf_input])
                # Atualizar session states
                if "fiadores" in dados_ficha:
                    st.session_state.fiadores = dados_ficha["fiadores"]
                if "comodos" in dados_ficha:
                    st.session_state.comodos = dados_ficha["comodos"]
                st.success(f"Dados carregados!")
            else:
                st.info("CPF não encontrado")

    # ----------------- Dados do Contrato / Locatário -----------------
    st.markdown('<div class="section-header"><h3>DADOS DO CONTRATO / LOCATÁRIO</h3></div>', unsafe_allow_html=True)
    
    # Linha 1
    col1, col2, col3 = st.columns(3)
    with col1:
        dados_ficha["nomeLocatario"] = st.text_input(
            "Nome do Locatário", 
            value=dados_ficha.get("nomeLocatario", ""),
            placeholder="Nome completo do locatário"
        )
    with col2:
        dados_ficha["RG"] = st.text_input(
            "RG", 
            value=dados_ficha.get("RG", ""),
            placeholder="00.000.000-0"
        )
    with col3:
        dados_ficha["CPFLocatario"] = st.text_input(
            "CPF do Locatário", 
            value=dados_ficha.get("CPFLocatario", ""),
            placeholder="000.000.000-00"
        )

    # Linha 2
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["endereco"] = st.text_input(
            "Endereço do Locatário", 
            value=dados_ficha.get("endereco", ""),
            placeholder="Rua, número, bairro"
        )
    with col2:
        dados_ficha["celular"] = st.text_input(
            "Celular", 
            value=dados_ficha.get("celular", ""),
            placeholder="(00) 00000-0000"
        )

    # Linha 3
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["email"] = st.text_input(
            "E-mail", 
            value=dados_ficha.get("email", ""),
            placeholder="email@exemplo.com"
        )
    with col2:
        dados_ficha["enderecoImovel"] = st.text_input(
            "Endereço do Imóvel", 
            value=dados_ficha.get("enderecoImovel", ""),
            placeholder="Endereço do imóvel vistoriado"
        )

    # Linha 4 - Datas
    col1, col2, col3 = st.columns(3)
    with col1:
        dados_ficha["dataContrato"] = st.text_input(
            "Data do Contrato", 
            value=dados_ficha.get("dataContrato", ""),
            placeholder="DD/MM/AAAA"
        )
    with col2:
        dados_ficha["dataVistoria"] = st.text_input(
            "Data da Vistoria", 
            value=dados_ficha.get("dataVistoria", ""),
            placeholder="DD/MM/AAAA"
        )
    with col3:
        dados_ficha["nomeVistoriador"] = st.text_input(
            "Nome do Vistoriador", 
            value=dados_ficha.get("nomeVistoriador", ""),
            placeholder="Nome do vistoriador"
        )

    # Linha 5 - Data do Termo
    col1, col2, col3 = st.columns(3)
    with col1:
        dados_ficha["dia"] = st.text_input("Dia", value=dados_ficha.get("dia", ""), placeholder="DD")
    with col2:
        dados_ficha["mes"] = st.text_input("Mês", value=dados_ficha.get("mes", ""), placeholder="MM")
    with col3:
        dados_ficha["ano"] = st.text_input("Ano", value=dados_ficha.get("ano", ""), placeholder="AAAA")

    # ----------------- Testemunhas -----------------
    st.markdown('<div class="section-header"><h3>TESTEMUNHAS</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        dados_ficha["TESTEMUNHA1"] = st.text_input(
            "Testemunha 1", 
            value=dados_ficha.get("TESTEMUNHA1", ""),
            placeholder="Nome da testemunha"
        )
        dados_ficha["CPFTestemunha1"] = st.text_input(
            "CPF Testemunha 1", 
            value=dados_ficha.get("CPFTestemunha1", ""),
            placeholder="000.000.000-00"
        )
    with col2:
        dados_ficha["TESTEMUNHA2"] = st.text_input(
            "Testemunha 2", 
            value=dados_ficha.get("TESTEMUNHA2", ""),
            placeholder="Nome da testemunha"
        )
        dados_ficha["CPFTestemunha2"] = st.text_input(
            "CPF Testemunha 2", 
            value=dados_ficha.get("CPFTestemunha2", ""),
            placeholder="000.000.000-00"
        )

    # ----------------- Fiadores -----------------
    st.markdown('<div class="section-header"><h3>FIADORES</h3></div>', unsafe_allow_html=True)
    
    fiadores = []
    for i in range(len(st.session_state.fiadores)):
        st.markdown(f"**Fiador {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input(
                f"Nome Fiador {i+1}", 
                value=st.session_state.fiadores[i].get("nome", ""), 
                key=f"fiador_nome_{i}",
                placeholder="Nome completo"
            )
            cpf = st.text_input(
                f"CPF Fiador {i+1}", 
                value=st.session_state.fiadores[i].get("cpf", ""), 
                key=f"fiador_cpf_{i}",
                placeholder="000.000.000-00"
            )
            rg = st.text_input(
                f"RG Fiador {i+1}", 
                value=st.session_state.fiadores[i].get("rg", ""), 
                key=f"fiador_rg_{i}",
                placeholder="00.000.000-0"
            )
        with col2:
            endereco = st.text_input(
                f"Endereço Fiador {i+1}", 
                value=st.session_state.fiadores[i].get("endereco", ""), 
                key=f"fiador_end_{i}",
                placeholder="Endereço completo"
            )
            telefone = st.text_input(
                f"Telefone Fiador {i+1}", 
                value=st.session_state.fiadores[i].get("telefone", ""), 
                key=f"fiador_tel_{i}",
                placeholder="(00) 00000-0000"
            )
        
        fiadores.append({
            "nome": nome,
            "cpf": cpf,
            "rg": rg,
            "endereco": endereco,
            "telefone": telefone
        })
    
    # Botões fiadores
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Adicionar Fiador", use_container_width=True):
            st.session_state.fiadores.append({})
            st.rerun()
    with col2:
        if len(st.session_state.fiadores) > 1 and st.button("➖ Remover Fiador", use_container_width=True):
            st.session_state.fiadores.pop()
            st.rerun()
    
    dados_ficha["fiadores"] = fiadores

    # ----------------- Cômodos -----------------
    st.markdown('<div class="section-header"><h3>CÔMODOS E CARACTERÍSTICAS</h3></div>', unsafe_allow_html=True)
    
    comodos_contexto = []
    for i, comodo in enumerate(st.session_state.comodos):
        st.markdown(f"**Cômodo {i+1}**")
        
        # Nome do cômodo
        nome_comodo = st.text_input(
            f"Nome do Cômodo {i+1}", 
            value=comodo["nome"], 
            key=f"comodo_nome_{i}",
            placeholder="Ex: Sala, Quarto, Cozinha"
        )
        
        # Características
        st.markdown("**Características:**")
        caracteristicas = []
        for j, carac in enumerate(comodo["caracteristicas"]):
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                nome_carac = st.text_input(
                    "Característica", 
                    value=carac["nome"], 
                    key=f"carac_nome_{i}_{j}",
                    placeholder="Ex: Piso, Parede, Tomada"
                )
            with col2:
                estado = st.selectbox(
                    "Estado", 
                    ["Bom", "Regular", "Ruim"], 
                    index=["Bom", "Regular", "Ruim"].index(carac["estado"]), 
                    key=f"carac_estado_{i}_{j}"
                )
            with col3:
                descricao = st.text_input(
                    "Descrição", 
                    value=carac["descricao"], 
                    key=f"carac_desc_{i}_{j}",
                    placeholder="Observações adicionais"
                )
            
            caracteristicas.append({
                "nome": nome_carac,
                "estado": estado,
                "descricao": descricao
            })
        
        comodos_contexto.append({
            "nome": nome_comodo,
            "caracteristicas": caracteristicas
        })
    
    # Botões para gerenciar cômodos
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Novo Cômodo", use_container_width=True):
            st.session_state.comodos.append({
                "nome": f"Cômodo {len(st.session_state.comodos) + 1}",
                "caracteristicas": [
                    {"nome": "Piso", "estado": "Bom", "descricao": ""},
                    {"nome": "Parede", "estado": "Bom", "descricao": ""}
                ]
            })
            st.rerun()
    with col2:
        if st.button("➕ Nova Característica", use_container_width=True):
            for comodo in st.session_state.comodos:
                comodo["caracteristicas"].append({
                    "nome": "Nova Característica",
                    "estado": "Bom",
                    "descricao": ""
                })
            st.rerun()
    with col3:
        if len(st.session_state.comodos) > 1 and st.button("➖ Remover Cômodo", use_container_width=True):
            st.session_state.comodos.pop()
            st.rerun()
    
    dados_ficha["comodos"] = comodos_contexto

    # ----------------- Botão Gerar Documento -----------------
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 GERAR TERMO DE VISTORIA", 
                    use_container_width=True, 
                    type="primary"):
            
            try:
                # Salvar dados no JSON (se houver CPF)
                cpf_key = dados_ficha.get("CPFLocatario")
                if cpf_key:
                    # Atualizar session state
                    st.session_state.fiadores = fiadores
                    st.session_state.comodos = comodos_contexto
                    
                    dados_todos[cpf_key] = dados_ficha
                    salvar_dados(dados_todos)
                    st.success("✅ Dados salvos com sucesso!")
                else:
                    st.info("ℹ️ Dados não salvos - CPF não informado")
                
                # Gerar documento (agora funciona mesmo sem CPF)
                doc = DocxTemplate(CAMINHO_TEMPLATE)
                doc.render(dados_ficha)
                
                # Salvar em memória
                buffer = BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                
                # Nome do arquivo
                nome_locatario = dados_ficha.get("nomeLocatario", "SemNome").replace(" ", "_")
                data_atual = datetime.today().strftime("%Y-%m-%d")
                nome_arquivo = f"Termo_Vistoria_{nome_locatario}_{data_atual}.docx"
                
                # Botão de download
                st.success("✅ Termo de Vistoria gerado com sucesso!")
                st.download_button(
                    label="📥 BAIXAR TERMO DE VISTORIA",
                    data=buffer,
                    file_name=nome_arquivo,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ Erro ao gerar documento: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Executar -----------------
if __name__ == "__main__":
    app()