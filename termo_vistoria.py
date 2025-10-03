import streamlit as st
from docxtpl import DocxTemplate, RichText
import os, json
from datetime import datetime
from io import BytesIO

# ----------------- Configurações -----------------
ARQUIVO_DADOS = "dados_vistorias.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

dados_todos = carregar_dados()

# ----------------- Função Principal -----------------
def app():
    from theme import apply_theme
    apply_theme()
    
    st.title("📋 GERADOR DE TERMO DE VISTORIA")

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
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
                padding: 10px;
                background-color: #f0f2f6;
                border-radius: 8px;
            }
            .comodo-container {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                border-left: 4px solid #4CAF50;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Inicializar session states
    if "fiadores" not in st.session_state:
        st.session_state.fiadores = [{"nome": "", "cpf": "", "rg": "", "endereco": "", "telefone": ""}]
    
    if "comodos" not in st.session_state:
        st.session_state.comodos = [{
            "nome": "Sala", 
            "caracteristicas": [
                {"nome": "Piso", "estado": "Bom", "descricao": ""},
                {"nome": "Parede", "estado": "Bom", "descricao": ""},
                {"nome": "Tomada", "estado": "Bom", "descricao": ""}
            ]
        }]

    # ----------------- CPF e Busca -----------------
    st.markdown('<div class="section-header"><h3>BUSCAR DADOS EXISTENTES</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        cpf_input = st.text_input("CPF do Locatário", key="cpf_vistoria", placeholder="000.000.000-00")
    with col2:
        if st.button("🔍 Carregar Dados", use_container_width=True):
            if cpf_input in dados_todos:
                dados_carregados = dados_todos[cpf_input]
                # Atualizar session states
                if "fiadores" in dados_carregados:
                    st.session_state.fiadores = dados_carregados["fiadores"]
                if "comodos" in dados_carregados:
                    st.session_state.comodos = dados_carregados["comodos"]
                st.success(f"Dados carregados para CPF {cpf_input}")
                st.rerun()
            else:
                st.info(f"Nenhum dado encontrado para CPF {cpf_input}")

    # ----------------- Dados do Locatário -----------------
    st.markdown('<div class="section-header"><h3>DADOS DO LOCATÁRIO</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        nomeLocatario = st.text_input("Nome do Locatário", value="", placeholder="Nome completo")
    with col2:
        RG = st.text_input("RG", value="", placeholder="00.000.000-0")
    with col3:
        CPFLocatario = st.text_input("CPF do Locatário", value=cpf_input, placeholder="000.000.000-00")

    col1, col2 = st.columns(2)
    with col1:
        endereco = st.text_input("Endereço do Locatário", value="", placeholder="Rua, número, bairro")
    with col2:
        celular = st.text_input("Celular", value="", placeholder="(00) 00000-0000")

    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("E-mail", value="", placeholder="email@exemplo.com")
    with col2:
        enderecoImovel = st.text_input("Endereço do Imóvel", value="", placeholder="Endereço completo do imóvel")

    # ----------------- Datas -----------------
    st.markdown('<div class="section-header"><h3>DATAS</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        dataContrato = st.text_input("Data do Contrato", value="", placeholder="DD/MM/AAAA")
    with col2:
        dataVistoria = st.text_input("Data da Vistoria", value="", placeholder="DD/MM/AAAA")
    with col3:
        nomeVistoriador = st.text_input("Nome do Vistoriador", value="", placeholder="Nome do vistoriador")

    col1, col2, col3 = st.columns(3)
    with col1:
        dia = st.text_input("Dia do Contrato", value="", placeholder="DD")
    with col2:
        mes = st.text_input("Mês do Contrato", value="", placeholder="ex: setembro")
    with col3:
        ano = st.text_input("Ano do Contrato", value="", placeholder="AAAA")

    # ----------------- Testemunhas -----------------
    st.markdown('<div class="section-header"><h3>TESTEMUNHAS</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        TESTEMUNHA1 = st.text_input("Testemunha 1", value="", placeholder="Nome completo")
        CPFTestemunha1 = st.text_input("CPF Testemunha 1", value="", placeholder="000.000.000-00")
    with col2:
        TESTEMUNHA2 = st.text_input("Testemunha 2", value="", placeholder="Nome completo")
        CPFTestemunha2 = st.text_input("CPF Testemunha 2", value="", placeholder="000.000.000-00")

    # ----------------- Fiadores -----------------
    st.markdown('<div class="section-header"><h3>FIADORES</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Adicionar Fiador", use_container_width=True):
            st.session_state.fiadores.append({"nome": "", "cpf": "", "rg": "", "endereco": "", "telefone": ""})
            st.rerun()
    with col2:
        if len(st.session_state.fiadores) > 1 and st.button("➖ Remover Fiador", use_container_width=True):
            st.session_state.fiadores.pop()
            st.rerun()

    # Formulário dos fiadores
    fiadores_richtext = []
    for idx, f in enumerate(st.session_state.fiadores):
        st.markdown(f"**Fiador {idx+1}**")
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input(f"Nome Fiador {idx+1}", value=f.get("nome", ""), key=f"fiador_nome_{idx}", placeholder="Nome completo")
            cpf = st.text_input(f"CPF Fiador {idx+1}", value=f.get("cpf", ""), key=f"fiador_cpf_{idx}", placeholder="000.000.000-00")
        with col2:
            rg = st.text_input(f"RG Fiador {idx+1}", value=f.get("rg", ""), key=f"fiador_rg_{idx}", placeholder="0000000")
            telefone = st.text_input(f"Telefone Fiador {idx+1}", value=f.get("telefone", ""), key=f"fiador_tel_{idx}", placeholder="(00) 00000-0000")
        
        endereco_fiador = st.text_input(f"Endereço Fiador {idx+1}", value=f.get("endereco", ""), key=f"fiador_end_{idx}", placeholder="Endereço completo")
        
        # Atualizar session state
        st.session_state.fiadores[idx] = {
            "nome": nome,
            "cpf": cpf, 
            "rg": rg,
            "endereco": endereco_fiador,
            "telefone": telefone
        }
        
        # Preparar RichText com títulos em NEGRITO
        if nome.strip():
            rt = RichText()
            rt.add("Nome: ", bold=True)
            rt.add(f"{nome}\n")
            rt.add("CPF: ", bold=True)
            rt.add(f"{cpf}\n")
            rt.add("RG: ", bold=True)
            rt.add(f"{rg}\n")
            rt.add("Endereço: ", bold=True)
            rt.add(f"{endereco_fiador}\n")
            rt.add("Telefone: ", bold=True)
            rt.add(f"{telefone}\n")
            fiadores_richtext.append(rt)

    # ----------------- Cômodos -----------------
    st.markdown('<div class="section-header"><h3>CÔMODOS E CARACTERÍSTICAS</h3></div>', unsafe_allow_html=True)
    
    # Botão para adicionar novo cômodo
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Adicionar Novo Cômodo", use_container_width=True):
            st.session_state.comodos.append({
                "nome": f"Cômodo {len(st.session_state.comodos) + 1}",
                "caracteristicas": [
                    {"nome": "Piso", "estado": "Bom", "descricao": ""},
                    {"nome": "Parede", "estado": "Bom", "descricao": ""}
                ]
            })
            st.rerun()
    with col2:
        if len(st.session_state.comodos) > 1 and st.button("➖ Remover Último Cômodo", use_container_width=True):
            st.session_state.comodos.pop()
            st.rerun()

    # Formulário dos cômodos
    comodos_para_template = []
    for i, comodo in enumerate(st.session_state.comodos):
        with st.container():
            st.markdown(f"""
            <div class="comodo-container">
                <h4>🏠 Cômodo {i+1}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Nome do cômodo
            nome_comodo = st.text_input(f"Nome do Cômodo {i+1}", value=comodo["nome"], key=f"comodo_nome_{i}", placeholder="Ex: Sala, Quarto, Cozinha")
            
            # Botão para adicionar característica APENAS neste cômodo
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"➕ Característica no Cômodo {i+1}", key=f"add_carac_{i}", use_container_width=True):
                    st.session_state.comodos[i]["caracteristicas"].append({
                        "nome": "Nova Característica",
                        "estado": "Bom",
                        "descricao": ""
                    })
                    st.rerun()
            with col2:
                if len(st.session_state.comodos[i]["caracteristicas"]) > 1 and st.button(f"➖ Remover Última do Cômodo {i+1}", key=f"remove_carac_{i}", use_container_width=True):
                    st.session_state.comodos[i]["caracteristicas"].pop()
                    st.rerun()
            
            # Características do cômodo
            caracteristicas_comodo = []
            for j, carac in enumerate(comodo["caracteristicas"]):
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    nome_carac = st.text_input("Característica", value=carac["nome"], key=f"carac_nome_{i}_{j}", placeholder="Ex: Piso, Parede, Tomada")
                with col2:
                    estado = st.selectbox("Estado", ["Bom", "Regular", "Ruim"], 
                                        index=["Bom", "Regular", "Ruim"].index(carac["estado"]), 
                                        key=f"carac_estado_{i}_{j}")
                with col3:
                    descricao = st.text_input("Descrição", value=carac["descricao"], key=f"carac_desc_{i}_{j}", placeholder="Observações")
                
                # Atualizar session state
                st.session_state.comodos[i]["caracteristicas"][j] = {
                    "nome": nome_carac,
                    "estado": estado,
                    "descricao": descricao
                }
                
                # Adicionar à lista de características
                caracteristicas_comodo.append({
                    "nome": nome_carac,
                    "estado": estado,
                    "descricao": descricao
                })
            
            # Atualizar nome do cômodo no session state
            st.session_state.comodos[i]["nome"] = nome_comodo
            
            # Preparar estrutura para template
            if nome_comodo.strip():
                comodos_para_template.append({
                    "nome": nome_comodo,
                    "caracteristicas": caracteristicas_comodo
                })
            
            st.markdown("---")

    # ----------------- Botão Gerar Documento -----------------
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 GERAR TERMO DE VISTORIA", use_container_width=True, type="primary"):
            try:
                # Preparar dados para salvar
                dados_para_salvar = {
                    "nomeLocatario": nomeLocatario,
                    "RG": RG,
                    "CPFLocatario": CPFLocatario,
                    "endereco": endereco,
                    "celular": celular,
                    "email": email,
                    "enderecoImovel": enderecoImovel,
                    "dataContrato": dataContrato,
                    "dataVistoria": dataVistoria,
                    "nomeVistoriador": nomeVistoriador,
                    "dia": dia,
                    "mes": mes,
                    "ano": ano,
                    "TESTEMUNHA1": TESTEMUNHA1,
                    "CPFTestemunha1": CPFTestemunha1,
                    "TESTEMUNHA2": TESTEMUNHA2,
                    "CPFTestemunha2": CPFTestemunha2,
                    "fiadores": st.session_state.fiadores,
                    "comodos": st.session_state.comodos
                }
                
                # Salvar dados no JSON
                cpf_key = CPFLocatario or cpf_input
                if cpf_key:
                    dados_todos[cpf_key] = dados_para_salvar
                    salvar_dados(dados_todos)
                    st.success("✅ Dados salvos com sucesso!")
                
                # Verificar template
                template_path = "vistoria_corrigido_dinamico.docx"
                if not os.path.exists(template_path):
                    st.error(f"❌ Template não encontrado: {template_path}")
                    return
                
                st.info("🔄 Gerando documento...")
                
                # Gerar documento
                doc = DocxTemplate(template_path)
                
                # Preparar dados para o template
                context = {
                    'nomeLocatario': nomeLocatario,
                    'RG': RG,
                    'CPFLocatario': CPFLocatario,
                    'endereco': endereco,
                    'celular': celular,
                    'email': email,
                    'fiadores': fiadores_richtext,  # RichText para fiadores
                    'enderecoImovel': enderecoImovel,
                    'dataContrato': dataContrato,
                    'comodos': comodos_para_template,  # Estrutura para loop
                    'TESTEMUNHA1': TESTEMUNHA1,
                    'CPFTestemunha1': CPFTestemunha1,
                    'TESTEMUNHA2': TESTEMUNHA2,
                    'CPFTestemunha2': CPFTestemunha2,
                    'nomeVistoriador': nomeVistoriador,
                    'dataVistoria': dataVistoria,
                    'dia': dia,
                    'mes': mes,
                    'ano': ano,
                }
                
                doc.render(context)
                
                # Salvar em memória
                buffer = BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                
                # Verificar se o buffer tem conteúdo
                if buffer.getbuffer().nbytes == 0:
                    st.error("❌ O documento gerado está vazio")
                    return
                
                # Nome do arquivo
                nome_locatario = nomeLocatario.replace(" ", "_") if nomeLocatario else "SemNome"
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
                import traceback
                st.error(f"Detalhes: {traceback.format_exc()}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Executar -----------------
if __name__ == "__main__":
    app()
    