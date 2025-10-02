import streamlit as st
from docxtpl import DocxTemplate
import os
from datetime import datetime
from io import BytesIO

# ----------------- Caminhos relativos -----------------
base_dir = os.path.dirname(__file__)  # pasta do script
CAMINHO_DOCX = os.path.join(base_dir, "Ficha_de_captacao.docx")  # template

def gerar_ficha(dados):
    try:
        if not os.path.exists(CAMINHO_DOCX):
            st.error(f"Arquivo {CAMINHO_DOCX} não encontrado.")
            return

        doc = DocxTemplate(CAMINHO_DOCX)
        doc.render(dados)

        endereco = dados.get("enderecoImovel", "SemEndereco").strip().replace(" ", "_")
        data_atual = datetime.today().strftime("%Y-%m-%d")
        nome_arquivo = f"Ficha_{endereco}_{data_atual}.docx"

        # 🔹 salvar apenas em memória
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.success("✅ Ficha gerada com sucesso!")
        st.download_button(
            label="📥 Baixar Ficha de Captação",
            data=buffer,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key="download_ficha_captacao"
        )
    except Exception as e:
        st.error(f"Erro ao gerar ficha: {e}")

def app():
    st.set_page_config(page_title="Ficha de Captação", layout="centered")
    
    # CSS para centralizar e estilizar
    st.markdown("""
        <style>
            .main-container {
                max-width: 900px;
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
            .section-container {
                margin: 20px 0;
                padding: 15px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #fafafa;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.title("🏠 FICHA DE CAPTAÇÃO")

    # Verificação do template
    if not os.path.exists(CAMINHO_DOCX):
        st.markdown(f"""
        <div class="warning-box">
            <h3>⚠️ Template Não Encontrado</h3>
            <p>O arquivo <strong>{CAMINHO_DOCX}</strong> não foi encontrado.</p>
            <p><strong>Por favor verifique:</strong></p>
            <ol>
                <li>Se o arquivo <strong>'Ficha_de_captacao.docx'</strong> está na mesma pasta do script</li>
                <li>O nome exato do arquivo (incluindo letras maiúsculas/minúsculas)</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success(f"✅ Template encontrado: {CAMINHO_DOCX}")

    secoes = {
        "💰 VALOR / TIPO DE NEGÓCIO": [
            ("valor","text","Valor (R$)"), ("aluguel","checkbox","Aluguel"), ("venda","checkbox","Venda")
        ],
        "🏘️ TIPO DE IMÓVEL": [
            ("casa","checkbox","Casa"), ("Apto","checkbox","Apto"), ("Sitio","checkbox","Sítio"),
            ("lotes","checkbox","Lotes"), ("outros","checkbox","Outros")
        ],
        "📋 DADOS DO IMÓVEL": [
            ("enderecoImovel","text","Endereço"), ("nImovel","text","Nº"), ("compl","text","Compl"),
            ("bairroImovel","text","Bairro"), ("cidadeImovel","text","Cidade"), ("UFImovel","text","UF"),
            ("quartoImovel","text","Quarto"), ("suiteImovel","text","Suíte"), ("cozinhImovel","text","Cozinha"),
            ("ATImovel","text","Área Total (ÁT)"), ("salaImovel","text","Sala"), ("copaImovel","text","Copa"),
            ("banheiroImovel","text","Banheiro"), ("ACImovel","text","Área Construída (ÁC)"),
            ("Quintal","text","Quintal"), ("GaragemImovel","text","Garagem"), ("areaServImovel","text","Área de Serviço"),
            ("revestimento","text","Revestimento"), ("esquadrilha","text","Esquadrilha"), ("piso","text","Piso"),
            ("situacao","text","Situação"), ("visitas","text","Visitas"), ("divulgacao","text","Divulgação"),
            ("IPTU","text","IPTU"), ("localizacao","text","Referência/Localização"), ("observacoes","text","Observações")
        ],
        "⭐ CARACTERÍSTICAS / INFRAESTRUTURA": [
            ("interfone","checkbox","Interfone"), ("areaPriv","checkbox","Área Privativa"), ("CHURRASQUEIRA","checkbox","Churrasqueira"),
            ("sala_de_jogos","checkbox","Salão de Jogos"), ("lavabo","checkbox","Lavabo"), ("ArmQuarto","checkbox","Arm. Quartos"),
            ("AQsOLAR","checkbox","Aquec. Solar"), ("salaoFests","checkbox","Salão de Festas"), ("despensa","checkbox","Despensa"),
            ("armCozinha","checkbox","Arm. Cozinha"), ("Aqgas","checkbox","Aquec. Gás"), ("numerodepavimentos","checkbox","N° Pavimentos"),
            ("DCE","checkbox","DCE"), ("boxBanehir","checkbox","Box Banheiro"), ("aquec.eletrico","checkbox","Aquec. Elétrico"),
            ("numeroapto","checkbox","N° Apto/Andar"), ("varanda","checkbox","Varanda"), ("areaLazer","checkbox","Área de Lazer"),
            ("porteiroFísico","checkbox","Porteiro Físico"), ("garagem","checkbox","Garagem L/I"), ("rouparia","checkbox","Rouparia"),
            ("closet","checkbox","Closet"), ("sauna","checkbox","Sauna"), ("nelevador","checkbox","N° Elevador"), ("box","checkbox","Box Despejo"),
            ("salaGinastica","checkbox","Sala Ginástica"), ("piscina","checkbox","Piscina"), ("escritorio","checkbox","Escritório"),
            ("AREACLARIDAD","checkbox","Área Claridade"), ("playground","checkbox","Playground"), ("salaTV","checkbox","Sala de TV"),
            ("SACADA","checkbox","Sacada"), ("quadra","checkbox","Quadra de Esporte"), ("topografia","checkbox","Topografia")
        ],
        "👤 DADOS DO PROPRIETÁRIO": [
            ("nomeProprietario","text","Nome"), ("ederecoProprietario","text","Endereço"), ("numeroProprietario","text","Nº"),
            ("CompleProprietario","text","Compl"), ("bairroProprietario","text","Bairro"), ("cidadeProprietario","text","Cidade"),
            ("UFPropritario","text","UF"), ("CpfProprietario","text","CPF"), ("RGProprietario","text","RG"),
            ("emailProprietario","text","E-mail"), ("telefoneProprietario","text","Tel. Fixo"),
            ("celularProprietario","text","Celular"), ("nomeCaptador","text","Captador"),
            ("dia","text","Dia"), ("mes","text","Mês"), ("ano","text","Ano")
        ],
        "🔑 SITUAÇÃO DAS CHAVES": [
            ("copiaVillares","checkbox","Cópia Villares"), ("copiaProprietario","checkbox","Cópia Proprietário")
        ]
    }

    dados_ficha = {}
    
    # Renderizar todas as seções fixas (sem expanders)
    for secao, campos in secoes.items():
        st.markdown(f'<div class="section-header"><h3>{secao}</h3></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        
        col_count = 3
        cols = st.columns(col_count)
        col_index = 0
        
        for campo, tipo, label in campos:
            key_name = campo + "_captacao"
            if tipo == "text":
                dados_ficha[campo] = st.text_input(label, key=key_name, placeholder=f"Digite {label.lower()}")
            elif tipo == "checkbox":
                dados_ficha[campo] = "✓" if cols[col_index].checkbox(label, key=key_name) else ""
                col_index = (col_index + 1) % col_count
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ----------------- Botão Gerar Documento -----------------
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 GERAR FICHA DE CAPTAÇÃO", use_container_width=True, type="primary", key="gerar_ficha_captacao"):
            gerar_ficha(dados_ficha)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Adicione estas linhas no final do arquivo:
if __name__ == "__main__":
    app()