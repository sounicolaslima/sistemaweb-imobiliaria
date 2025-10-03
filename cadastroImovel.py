import streamlit as st
import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate
import io
import os

# ----------------- Configuração da página -----------------
st.set_page_config(
    page_title="Cadastro de Imóvel - Gerador de Ficha",
    page_icon="🏠",
    layout="wide"
)

# ----------------- Estilo CSS -----------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e86ab;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #2e86ab;
    }
    .stButton button {
        width: 100%;
        background-color: #2e86ab;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border: none;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Título principal -----------------
st.markdown('<div class="main-header">🏠 CADASTRO DE IMÓVEL</div>', unsafe_allow_html=True)

# ----------------- Inicialização do estado da sessão -----------------
if 'dados_formulario' not in st.session_state:
    st.session_state.dados_formulario = {}

# ----------------- Funções auxiliares -----------------
def criar_colunas(num_cols, padding_top=0):
    return st.columns(num_cols)

# ----------------- Formulário principal -----------------
with st.form("formulario_imovel"):

    # Seção: Valor / Tipo de Negócio
    st.markdown('<div class="section-header">💰 Valor / Tipo de Negócio</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = criar_colunas(3)
    with col1:
        valor = st.text_input("Valor (R$)", placeholder="Ex: 250.000,00")
    with col2:
        st.write("Tipo de Negócio")
        aluguel = st.checkbox("Aluguel", value=True)
        venda = st.checkbox("Venda")
    with col3:
        st.write("&nbsp;")  # Espaçamento

    # Seção: Tipo de Imóvel
    st.markdown('<div class="section-header">🏡 Tipo de Imóvel</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = criar_colunas(5)
    with col1:
        casa = st.checkbox("Casa")
    with col2:
        apto = st.checkbox("Apartamento")
    with col3:
        sitio = st.checkbox("Sítio")
    with col4:
        lotes = st.checkbox("Lotes")
    with col5:
        outros = st.checkbox("Outros")

    # Seção: Dados do Imóvel
    st.markdown('<div class="section-header">📋 Dados do Imóvel</div>', unsafe_allow_html=True)
    
    # Linha 1 - Endereço
    col1, col2, col3 = criar_colunas(3)
    with col1:
        endereco_imovel = st.text_input("Endereço", placeholder="Rua, Avenida, etc.")
    with col2:
        n_imovel = st.text_input("Número", placeholder="123")
    with col3:
        compl = st.text_input("Complemento", placeholder="Apto, Bloco, etc.")

    # Linha 2 - Bairro, Cidade, UF
    col1, col2, col3 = criar_colunas(3)
    with col1:
        bairro_imovel = st.text_input("Bairro", placeholder="Centro")
    with col2:
        cidade_imovel = st.text_input("Cidade", placeholder="Lavras")
    with col3:
        uf_imovel = st.text_input("UF", placeholder="MG", max_chars=2)

    # Linha 3 - Quartos, Suítes, Cozinha
    col1, col2, col3, col4 = criar_colunas(4)
    with col1:
        quarto_imovel = st.text_input("Quartos", placeholder="3")
    with col2:
        suite_imovel = st.text_input("Suítes", placeholder="1")
    with col3:
        cozinha_imovel = st.text_input("Cozinhas", placeholder="1")
    with col4:
        at_imovel = st.text_input("Área Total (m²)", placeholder="150")

    # Linha 4 - Salas, Copa, Banheiro, Área Construída
    col1, col2, col3, col4 = criar_colunas(4)
    with col1:
        sala_imovel = st.text_input("Salas", placeholder="2")
    with col2:
        copa_imovel = st.text_input("Copas", placeholder="1")
    with col3:
        banheiro_imovel = st.text_input("Banheiros", placeholder="2")
    with col4:
        ac_imovel = st.text_input("Área Construída (m²)", placeholder="120")

    # Linha 5 - Quintal, Garagem, Área de Serviço
    col1, col2, col3 = criar_colunas(3)
    with col1:
        quintal = st.text_input("Quintal", placeholder="Sim/Não")
    with col2:
        garagem_imovel = st.text_input("Vagas Garagem", placeholder="2")
    with col3:
        area_serv_imovel = st.text_input("Área de Serviço", placeholder="Sim/Não")

    # Linha 6 - Revestimento, Esquadrilha, Piso
    col1, col2, col3 = criar_colunas(3)
    with col1:
        revestimento = st.text_input("Revestimento", placeholder="Tipo de revestimento")
    with col2:
        esquadrilha = st.text_input("Esquadrilha", placeholder="Tipo de esquadrilha")
    with col3:
        piso = st.text_input("Piso", placeholder="Tipo de piso")

    # Linha 7 - Situação, Visitas, Divulgação, IPTU
    col1, col2, col3, col4 = criar_colunas(4)
    with col1:
        situacao = st.text_input("Situação", placeholder="Novo/Usado")
    with col2:
        visitas = st.text_input("Visitas", placeholder="Dias/horários")
    with col3:
        divulgacao = st.text_input("Meio de Divulgação", placeholder="Site, Jornal, etc.")
    with col4:
        iptu = st.text_input("IPTU", placeholder="Valor do IPTU")

    # Linha 8 - Referência/Localização
    localizacao = st.text_area("Referência/Localização", placeholder="Pontos de referência próximos")

    # Seção: Características do Imóvel / Infraestrutura
    st.markdown('<div class="section-header">🏊 Características do Imóvel / Infraestrutura</div>', unsafe_allow_html=True)
    
    # Organizando as características em 3 colunas
    col1, col2, col3 = criar_colunas(3)
    
    with col1:
        interfone = st.checkbox("Interfone")
        lavabo = st.checkbox("Lavabo")
        despensa = st.checkbox("Despensa")
        dce = st.checkbox("DCE")
        varanda = st.checkbox("Varanda")
        rouparia = st.checkbox("Rouparia")
        box = st.checkbox("Box Despejo")
        escritorio = st.checkbox("Escritório")
        sala_tv = st.checkbox("Sala de TV")
        
    with col2:
        area_priv = st.checkbox("Área Privativa")
        arm_quarto = st.checkbox("Arm. Quartos")
        arm_cozinha = st.checkbox("Arm. Cozinha")
        box_banheiro = st.checkbox("Box Banheiro")
        area_lazer = st.checkbox("Área de Lazer")
        closet = st.checkbox("Closet")
        sala_ginastica = st.checkbox("Sala Ginástica")
        area_claridade = st.checkbox("Área Claridade")
        sacada = st.checkbox("Sacada")
        
    with col3:
        churrasqueira = st.checkbox("Churrasqueira")
        aq_solar = st.checkbox("Aquec. Solar")
        aq_gas = st.checkbox("Aquec. Gás")
        aquec_eletrico = st.checkbox("Aquec. Elétrico")
        porteiro_fisico = st.checkbox("Porteiro Físico")
        sauna = st.checkbox("Sauna")
        piscina = st.checkbox("Piscina")
        playground = st.checkbox("Playground")
        quadra = st.checkbox("Quadra de Esporte")

    # Campos adicionais de infraestrutura
    col1, col2, col3, col4 = criar_colunas(4)
    with col1:
        numero_pavimentos = st.text_input("N° Pavimentos", placeholder="Ex: 5")
    with col2:
        numero_apto = st.text_input("N° Apto/Andar", placeholder="Ex: 2º andar")
    with col3:
        garagem_li = st.text_input("Garagem L/I", placeholder="Livre/Irregular")
    with col4:
        n_elevador = st.text_input("N° Elevadores", placeholder="Ex: 2")

    col1, col2 = criar_colunas(2)
    with col1:
        valor_cond = st.text_input("Valor Condomínio (R$)", placeholder="Ex: 300,00")
    with col2:
        met_frente = st.text_input("Metragem Frente", placeholder="Ex: 10m")

    topografia = st.text_input("Topografia", placeholder="Ex: Plano")

    # Observações
    observacoes = st.text_area("Observações", placeholder="Informações adicionais sobre o imóvel")

    # Seção: Dados do Proprietário
    st.markdown('<div class="section-header">👤 Dados do Proprietário</div>', unsafe_allow_html=True)
    
    # Linha 1 - Nome
    nome_proprietario = st.text_input("Nome Completo", placeholder="Nome do proprietário")

    # Linha 2 - Endereço
    col1, col2, col3 = criar_colunas(3)
    with col1:
        endereco_proprietario = st.text_input("Endereço", placeholder="Endereço do proprietário")
    with col2:
        numero_proprietario = st.text_input("Número", placeholder="Nº")
    with col3:
        compl_proprietario = st.text_input("Complemento", placeholder="Complemento")

    # Linha 3 - Bairro, Cidade, UF
    col1, col2, col3 = criar_colunas(3)
    with col1:
        bairro_proprietario = st.text_input("Bairro", placeholder="Bairro")
    with col2:
        cidade_proprietario = st.text_input("Cidade", placeholder="Cidade")
    with col3:
        uf_proprietario = st.text_input("UF", placeholder="UF", max_chars=2)

    # Linha 4 - CPF, RG, Email
    col1, col2, col3 = criar_colunas(3)
    with col1:
        cpf_proprietario = st.text_input("CPF", placeholder="000.000.000-00")
    with col2:
        rg_proprietario = st.text_input("RG", placeholder="RG")
    with col3:
        email_proprietario = st.text_input("E-mail", placeholder="email@exemplo.com")

    # Linha 5 - Telefones
    col1, col2 = criar_colunas(2)
    with col1:
        telefone_proprietario = st.text_input("Telefone Fixo", placeholder="(35) 3821-0000")
    with col2:
        celular_proprietario = st.text_input("Celular", placeholder="(35) 99999-0000")

    # Seção: Data e Captador
    st.markdown('<div class="section-header">📅 Data e Captador</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = criar_colunas(3)
    with col1:
        dia = st.text_input("Dia", placeholder="DD", value=datetime.now().strftime("%d"))
    with col2:
        mes = st.text_input("Mês", placeholder="MM", value=datetime.now().strftime("%m"))
    with col3:
        ano = st.text_input("Ano", placeholder="AAAA", value=datetime.now().strftime("%Y"))

    nome_captador = st.text_input("Nome do Captador", placeholder="Seu nome")

    # Seção: Situação das Chaves
    st.markdown('<div class="section-header">🔑 Situação das Chaves</div>', unsafe_allow_html=True)
    
    col1, col2 = criar_colunas(2)
    with col1:
        copia_villares = st.checkbox("Cópia Villares Imóveis")
    with col2:
        copia_proprietario = st.checkbox("Cópia do Proprietário")

    # Botão de envio
    submitted = st.form_submit_button("📄 Gerar Ficha de Captação")

# ----------------- Processamento do formulário -----------------
if submitted:
    try:
        # Preparar dados para o template
        dados_template = {
            # Valor e tipo
            "valor": valor,
            "aluguel": "✓" if aluguel else "",
            "venda": "✓" if venda else "",
            
            # Tipo de imóvel
            "casa": "✓" if casa else "",
            "Apto": "✓" if apto else "",
            "Sitio": "✓" if sitio else "",
            "lotes": "✓" if lotes else "",
            "outros": "✓" if outros else "",
            
            # Dados do imóvel
            "enderecoImovel": endereco_imovel,
            "nImovel": n_imovel,
            "compl": compl,
            "bairroImovel": bairro_imovel,
            "cidadeImovel": cidade_imovel,
            "UFImovel": uf_imovel,
            "quartoImovel": quarto_imovel,
            "suiteImovel": suite_imovel,
            "cozinhImovel": cozinha_imovel,
            "ATImovel": at_imovel,
            "salaImovel": sala_imovel,
            "copaImovel": copa_imovel,
            "banheiroImovel": banheiro_imovel,
            "ACImovel": ac_imovel,
            "Quintal": quintal,
            "GaragemImovel": garagem_imovel,
            "areaServImovel": area_serv_imovel,
            "revestimento": revestimento,
            "esquadrilha": esquadrilha,
            "piso": piso,
            "situacao": situacao,
            "visitas": visitas,
            "divulgacao": divulgacao,
            "IPTU": iptu,
            "localizacao": localizacao,
            "observacoes": observacoes,
            
            # Características
            "interfone": "✓" if interfone else "",
            "areaPriv": "✓" if area_priv else "",
            "churrasqueira": "✓" if churrasqueira else "",
            "sala_de_jogos": "✓" if st.session_state.get('sala_jogos') else "",
            "lavabo": "✓" if lavabo else "",
            "ArmQuarto": "✓" if arm_quarto else "",
            "AQsOLAR": "✓" if aq_solar else "",
            "salaoFests": "✓" if st.session_state.get('salao_festas') else "",
            "despensa": "✓" if despensa else "",
            "armCozinha": "✓" if arm_cozinha else "",
            "Aqgas": "✓" if aq_gas else "",
            "numerodepavimentos": numero_pavimentos,
            "DCE": "✓" if dce else "",
            "boxBanehir": "✓" if box_banheiro else "",
            "aquecEletrico": "✓" if aquec_eletrico else "",
            "numeroapto": numero_apto,
            "varanda": "✓" if varanda else "",
            "areaLazer": "✓" if area_lazer else "",
            "porteiroFísico": "✓" if porteiro_fisico else "",
            "garagem": garagem_li,
            "rouparia": "✓" if rouparia else "",
            "closet": "✓" if closet else "",
            "sauna": "✓" if sauna else "",
            "nelevador": n_elevador,
            "box": "✓" if box else "",
            "salaGinastica": "✓" if sala_ginastica else "",
            "piscina": "✓" if piscina else "",
            "escritorio": "✓" if escritorio else "",
            "AREACLARIDAD": "✓" if area_claridade else "",
            "playground": "✓" if playground else "",
            "salaTV": "✓" if sala_tv else "",
            "SACADA": "✓" if sacada else "",
            "quadra": "✓" if quadra else "",
            "topografia": topografia,
            "valorCond": valor_cond,
            "metFrente": met_frente,
            
            # Dados do proprietário
            "nomeProprietario": nome_proprietario,
            "ederecoProprietario": endereco_proprietario,
            "numeroProprietario": numero_proprietario,
            "CompleProprietario": compl_proprietario,
            "bairroProprietario": bairro_proprietario,
            "cidadeProprietario": cidade_proprietario,
            "UFPropritario": uf_proprietario,
            "CpfProprietario": cpf_proprietario,
            "RGProprietario": rg_proprietario,
            "emailProprietario": email_proprietario,
            "telefoneProprietario": telefone_proprietario,
            "celularProprietario": celular_proprietario,
            
            # Data e captador
            "dia": dia,
            "mes": mes,
            "ano": ano,
            "nomeCaptador": nome_captador,
            
            # Chaves
            "copiaVillares": "✓" if copia_villares else "",
            "copiaProprietario": "✓" if copia_proprietario else "",
        }
        
        # Carregar e processar o template
        doc = DocxTemplate("ficha_de_captacao.docx")
        doc.render(dados_template)
        
        # Salvar o documento
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        # Nome do arquivo
        endereco_formatado = endereco_imovel.replace(" ", "_").replace(",", "") if endereco_imovel else "SemEndereco"
        data_atual = datetime.now().strftime("%Y-%m-%d")
        nome_arquivo = f"Ficha_Captacao_{endereco_formatado}_{data_atual}.docx"
        
        # Botão de download
        st.success("✅ Ficha gerada com sucesso!")
        st.download_button(
            label="📥 Baixar Ficha de Captação",
            data=buffer,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        st.error(f"❌ Erro ao gerar a ficha: {str(e)}")
        st.info("ℹ️ Verifique se o arquivo 'ficha_de_captacao.docx' está na mesma pasta do aplicativo.")

# ----------------- Informações de uso -----------------
with st.expander("ℹ️ Instruções de Uso"):
    st.markdown("""
    **Como usar este formulário:**
    
    1. **Preencha os campos** que desejar (nenhum campo é obrigatório)
    2. **Selecione as características** do imóvel marcando as checkboxes correspondentes
    3. **Forneça os dados** do proprietário
    4. **Clique em 'Gerar Ficha de Captação'** para criar o documento
    5. **Baixe o arquivo** usando o botão que aparecerá após a geração
    
    **Observação:** 
    - Todos os campos são opcionais
    - O documento será gerado mesmo com campos em branco
    - Campos vazios aparecerão como espaços em branco no documento final
    """)

st.markdown("---")
st.markdown("**Villares Imóveis** - Sistema de Cadastro de Imóveis")