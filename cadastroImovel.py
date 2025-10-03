# cadastroImovel.py
import streamlit as st
from docxtpl import DocxTemplate
import os, json
from io import BytesIO
from datetime import datetime

def app():
    from theme import apply_theme
    apply_theme()
    
    # ----------------- Caminho relativo do arquivo Word -----------------
    base_dir = os.path.dirname(__file__)  # pasta onde está o script
    CAMINHO_DOCX = os.path.join(base_dir, "Ficha_de_captacao.docx")  # template

    # ----------------- Configuração da Página -----------------
    st.set_page_config(page_title="Cadastro de Imóvel", layout="wide")
    
    # CSS para centralizar e estilizar
    st.markdown("""
        <style>
            .main-container {
                max-width: 1200px;
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
            .checkbox-container {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # CORREÇÃO: Botão voltar no topo + compatibilidade
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "inicial"

    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ VOLTAR", use_container_width=True, key="voltar_cadastro_imovel"):
            st.session_state.pagina = "inicial"
            st.rerun()
    with col_title:
        st.title("🏠 CADASTRO DE IMÓVEL")

    # ----------------- Valor / Tipo de Negócio -----------------
    st.markdown('<div class="section-header"><h3>VALOR / TIPO DE NEGÓCIO</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        valor = st.text_input("Valor (R$)", placeholder="Ex: 250.000,00")
    with col2:
        st.write("Tipo de Negócio")
        aluguel = st.checkbox("Aluguel", value=True)
        venda = st.checkbox("Venda")

    # ----------------- Tipo de Imóvel -----------------
    st.markdown('<div class="section-header"><h3>TIPO DE IMÓVEL</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
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

    # ----------------- Dados do Imóvel -----------------
    st.markdown('<div class="section-header"><h3>DADOS DO IMÓVEL</h3></div>', unsafe_allow_html=True)
    
    # Linha 1 - Endereço
    col1, col2, col3 = st.columns(3)
    with col1:
        enderecoImovel = st.text_input("Endereço", placeholder="Rua, Avenida, etc.")
    with col2:
        nImovel = st.text_input("Número", placeholder="123")
    with col3:
        compl = st.text_input("Complemento", placeholder="Apto, Bloco, etc.")

    # Linha 2 - Bairro, Cidade, UF
    col1, col2, col3 = st.columns(3)
    with col1:
        bairroImovel = st.text_input("Bairro", placeholder="Centro")
    with col2:
        cidadeImovel = st.text_input("Cidade", placeholder="Lavras")
    with col3:
        UFImovel = st.text_input("UF", placeholder="MG", max_chars=2)

    # Linha 3 - Quartos, Suítes, Cozinha, Área Total
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        quartoImovel = st.text_input("Quartos", placeholder="3")
    with col2:
        suiteImovel = st.text_input("Suítes", placeholder="1")
    with col3:
        cozinhImovel = st.text_input("Cozinhas", placeholder="1")
    with col4:
        ATImovel = st.text_input("Área Total (m²)", placeholder="150")

    # Linha 4 - Salas, Copa, Banheiro, Área Construída
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        salaImovel = st.text_input("Salas", placeholder="2")
    with col2:
        copaImovel = st.text_input("Copas", placeholder="1")
    with col3:
        banheiroImovel = st.text_input("Banheiros", placeholder="2")
    with col4:
        ACImovel = st.text_input("Área Construída (m²)", placeholder="120")

    # Linha 5 - Quintal, Garagem, Área de Serviço
    col1, col2, col3 = st.columns(3)
    with col1:
        Quintal = st.text_input("Quintal", placeholder="Sim/Não")
    with col2:
        GaragemImovel = st.text_input("Vagas Garagem", placeholder="2")
    with col3:
        areaServImovel = st.text_input("Área de Serviço", placeholder="Sim/Não")

    # Linha 6 - Revestimento, Esquadrilha, Piso
    col1, col2, col3 = st.columns(3)
    with col1:
        revestimento = st.text_input("Revestimento", placeholder="Tipo de revestimento")
    with col2:
        esquadrilha = st.text_input("Esquadrilha", placeholder="Tipo de esquadrilha")
    with col3:
        piso = st.text_input("Piso", placeholder="Tipo de piso")

    # Linha 7 - Situação, Visitas, Divulgação, IPTU
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        situacao = st.text_input("Situação", placeholder="Novo/Usado")
    with col2:
        visitas = st.text_input("Visitas", placeholder="Dias/horários")
    with col3:
        divulgacao = st.text_input("Meio de Divulgação", placeholder="Site, Jornal, etc.")
    with col4:
        IPTU = st.text_input("IPTU", placeholder="Valor do IPTU")

    # Referência/Localização
    localizacao = st.text_area("Referência/Localização", placeholder="Pontos de referência próximos")

    # ----------------- Características do Imóvel -----------------
    st.markdown('<div class="section-header"><h3>CARACTERÍSTICAS DO IMÓVEL / INFRAESTRUTURA</h3></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        interfone = st.checkbox("Interfone")
        lavabo = st.checkbox("Lavabo")
        despensa = st.checkbox("Despensa")
        dce = st.checkbox("DCE")
        varanda = st.checkbox("Varanda")
        rouparia = st.checkbox("Rouparia")
        box = st.checkbox("Box Despejo")
        
    with col2:
        areaPriv = st.checkbox("Área Privativa")
        ArmQuarto = st.checkbox("Arm. Quartos")
        armCozinha = st.checkbox("Arm. Cozinha")
        boxBanehir = st.checkbox("Box Banheiro")
        areaLazer = st.checkbox("Área de Lazer")
        closet = st.checkbox("Closet")
        salaGinastica = st.checkbox("Sala Ginástica")
        
    with col3:
        churrasqueira = st.checkbox("Churrasqueira")
        AQsOLAR = st.checkbox("Aquec. Solar")
        Aqgas = st.checkbox("Aquec. Gás")
        aquecEletrico = st.checkbox("Aquec. Elétrico")
        porteiroFisico = st.checkbox("Porteiro Físico")
        sauna = st.checkbox("Sauna")
        piscina = st.checkbox("Piscina")
        
    with col4:
        sala_de_jogos = st.checkbox("Salão de Jogos")
        salaoFests = st.checkbox("Salão de Festas")
        numerodepavimentos = st.checkbox("N° Pavimentos")
        numeroapto = st.checkbox("N° Apto/Andar")
        garagem = st.checkbox("Garagem L/I")
        nelevador = st.checkbox("N° Elevador")
        playground = st.checkbox("Playground")
        quadra = st.checkbox("Quadra Esporte")
        AREACLARIDAD = st.checkbox("Área Claridade")
        SACADA = st.checkbox("Sacada")
        salaTV = st.checkbox("Sala de TV")
        escritorio = st.checkbox("Escritório")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------- Campos de Texto (3 últimas) -----------------
    st.markdown('<div class="section-header"><h3>INFORMAÇÕES ADICIONAIS</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        valorCond = st.text_input("Valor Condomínio (R$)", placeholder="Ex: 300,00")
    with col2:
        metFrente = st.text_input("Metragem Frente", placeholder="Ex: 10m")
    with col3:
        topografia = st.text_input("Topografia", placeholder="Ex: Plano")

    # Observações
    observacoes = st.text_area("Observações", placeholder="Informações adicionais sobre o imóvel")

    # ----------------- Dados do Proprietário -----------------
    st.markdown('<div class="section-header"><h3>DADOS DO PROPRIETÁRIO</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        nomeProprietario = st.text_input("Nome Completo", placeholder="Nome do proprietário")
        CpfProprietario = st.text_input("CPF", placeholder="000.000.000-00")
        ederecoProprietario = st.text_input("Endereço", placeholder="Endereço do proprietário")
        bairroProprietario = st.text_input("Bairro", placeholder="Bairro")
    
    with col2:
        RGProprietario = st.text_input("RG", placeholder="RG")
        emailProprietario = st.text_input("E-mail", placeholder="email@exemplo.com")
        numeroProprietario = st.text_input("Número", placeholder="Nº")
        cidadeProprietario = st.text_input("Cidade", placeholder="Cidade")

    col1, col2 = st.columns(2)
    with col1:
        telefoneProprietario = st.text_input("Telefone Fixo", placeholder="(35) 3821-0000")
    with col2:
        celularProprietario = st.text_input("Celular", placeholder="(35) 99999-0000")

    col1, col2, col3 = st.columns(3)
    with col1:
        CompleProprietario = st.text_input("Complemento", placeholder="Complemento")
    with col2:
        UFPropritario = st.text_input("UF", placeholder="UF", max_chars=2)

    # ----------------- Data e Captador -----------------
    st.markdown('<div class="section-header"><h3>DATA E CAPTADOR</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        dia = st.text_input("Dia", value=datetime.now().strftime("%d"), placeholder="DD")
    with col2:
        mes = st.text_input("Mês", value=datetime.now().strftime("%m"), placeholder="MM")
    with col3:
        ano = st.text_input("Ano", value=datetime.now().strftime("%Y"), placeholder="AAAA")

    nomeCaptador = st.text_input("Nome do Captador", placeholder="Seu nome")

    # ----------------- Situação das Chaves -----------------
    st.markdown('<div class="section-header"><h3>SITUAÇÃO DAS CHAVES</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        copiaVillares = st.checkbox("Cópia Villares Imóveis")
    with col2:
        copiaProprietario = st.checkbox("Cópia do Proprietário")

    # ----------------- Função gerar ficha -----------------
    def gerar_ficha_streamlit():
        if not os.path.exists(CAMINHO_DOCX):
            st.error(f"Arquivo {CAMINHO_DOCX} não encontrado.")
            return None

        doc = DocxTemplate(CAMINHO_DOCX)
        
        # Preparar todos os dados para o template
        dados = {
            # Valor e tipo
            "valor": valor or "",
            "aluguel": "✓" if aluguel else "",
            "venda": "✓" if venda else "",
            
            # Tipo de imóvel
            "casa": "✓" if casa else "",
            "Apto": "✓" if apto else "",
            "Sitio": "✓" if sitio else "",
            "lotes": "✓" if lotes else "",
            "outros": "✓" if outros else "",
            
            # Dados do imóvel
            "enderecoImovel": enderecoImovel or "",
            "nImovel": nImovel or "",
            "compl": compl or "",
            "bairroImovel": bairroImovel or "",
            "cidadeImovel": cidadeImovel or "",
            "UFImovel": UFImovel or "",
            "quartoImovel": quartoImovel or "",
            "suiteImovel": suiteImovel or "",
            "cozinhImovel": cozinhImovel or "",
            "ATImovel": ATImovel or "",
            "salaImovel": salaImovel or "",
            "copaImovel": copaImovel or "",
            "banheiroImovel": banheiroImovel or "",
            "ACImovel": ACImovel or "",
            "Quintal": Quintal or "",
            "GaragemImovel": GaragemImovel or "",
            "areaServImovel": areaServImovel or "",
            "revestimento": revestimento or "",
            "esquadrilha": esquadrilha or "",
            "piso": piso or "",
            "situacao": situacao or "",
            "visitas": visitas or "",
            "divulgacao": divulgacao or "",
            "IPTU": IPTU or "",
            "localizacao": localizacao or "",
            "observacoes": observacoes or "",
            
            # Características (TODAS como checkbox)
            "interfone": "✓" if interfone else "",
            "areaPriv": "✓" if areaPriv else "",
            "churrasqueira": "✓" if churrasqueira else "",
            "sala_de_jogos": "✓" if sala_de_jogos else "",
            "lavabo": "✓" if lavabo else "",
            "ArmQuarto": "✓" if ArmQuarto else "",
            "AQsOLAR": "✓" if AQsOLAR else "",
            "salaoFests": "✓" if salaoFests else "",
            "despensa": "✓" if despensa else "",
            "armCozinha": "✓" if armCozinha else "",
            "Aqgas": "✓" if Aqgas else "",
            "numerodepavimentos": "✓" if numerodepavimentos else "",
            "DCE": "✓" if dce else "",
            "boxBanehir": "✓" if boxBanehir else "",
            "aquecEletrico": "✓" if aquecEletrico else "",
            "numeroapto": "✓" if numeroapto else "",
            "varanda": "✓" if varanda else "",
            "areaLazer": "✓" if areaLazer else "",
            "porteiroFísico": "✓" if porteiroFisico else "",
            "garagem": "✓" if garagem else "",
            "rouparia": "✓" if rouparia else "",
            "closet": "✓" if closet else "",
            "sauna": "✓" if sauna else "",
            "nelevador": "✓" if nelevador else "",
            "box": "✓" if box else "",
            "salaGinastica": "✓" if salaGinastica else "",
            "piscina": "✓" if piscina else "",
            "escritorio": "✓" if escritorio else "",
            "AREACLARIDAD": "✓" if AREACLARIDAD else "",
            "playground": "✓" if playground else "",
            "salaTV": "✓" if salaTV else "",
            "SACADA": "✓" if SACADA else "",
            "quadra": "✓" if quadra else "",
            "topografia": topografia or "",  # Campo de texto
            "valorCond": valorCond or "",    # Campo de texto
            "metFrente": metFrente or "",    # Campo de texto
            
            # Dados do proprietário
            "nomeProprietario": nomeProprietario or "",
            "ederecoProprietario": ederecoProprietario or "",
            "numeroProprietario": numeroProprietario or "",
            "CompleProprietario": CompleProprietario or "",
            "bairroProprietario": bairroProprietario or "",
            "cidadeProprietario": cidadeProprietario or "",
            "UFPropritario": UFPropritario or "",
            "CpfProprietario": CpfProprietario or "",
            "RGProprietario": RGProprietario or "",
            "emailProprietario": emailProprietario or "",
            "telefoneProprietario": telefoneProprietario or "",
            "celularProprietario": celularProprietario or "",
            
            # Data e captador
            "dia": dia or "",
            "mes": mes or "",
            "ano": ano or "",
            "nomeCaptador": nomeCaptador or "",
            
            # Chaves
            "copiaVillares": "✓" if copiaVillares else "",
            "copiaProprietario": "✓" if copiaProprietario else "",
        }

        # Renderizar documento
        doc.render(dados)

        # Salvar apenas em memória
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer

    # ----------------- Botão gerar/download -----------------
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 GERAR FICHA DE CAPTAÇÃO", use_container_width=True, type="primary"):
            arquivo = gerar_ficha_streamlit()
            if arquivo:
                endereco_clean = enderecoImovel.replace(" ", "_") if enderecoImovel else "SemEndereco"
                data_atual = datetime.now().strftime("%Y-%m-%d")
                nome_arquivo = f"Ficha_Captacao_{endereco_clean}_{data_atual}.docx"

                st.success("✅ Ficha gerada com sucesso!")
                st.download_button(
                    label="📥 BAIXAR FICHA DE CAPTAÇÃO",
                    data=arquivo,
                    file_name=nome_arquivo,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
    
    # CORREÇÃO: REMOVIDO o fechamento do container
    # st.markdown('</div>', unsafe_allow_html=True) 
    
if __name__ == "__main__":
    app()