import streamlit as st
from docxtpl import DocxTemplate
import os
from datetime import datetime

CAMINHO_DOCX = "ficha_de_captacao.docx"

def gerar_ficha(dados):
    try:
        if not os.path.exists(CAMINHO_DOCX):
            st.error(f"Arquivo {CAMINHO_DOCX} não encontrado.")
            return

        doc = DocxTemplate(CAMINHO_DOCX)
        doc.render(dados)

        pasta_saida = "captacaoImoveis"
        os.makedirs(pasta_saida, exist_ok=True)

        endereco = dados.get("enderecoImovel", "SemEndereco").strip().replace(" ", "_")
        data_atual = datetime.today().strftime("%Y-%m-%d")
        nome_arquivo = f"Ficha_{endereco}_{data_atual}.docx"

        caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
        doc.save(caminho_arquivo)

        st.success("✅ Ficha gerada com sucesso!")
        with open(caminho_arquivo, "rb") as f:
            st.download_button("📥 Baixar Ficha de Captação", f, file_name=nome_arquivo, key="download_ficha_captacao")
    except Exception as e:
        st.error(f"Erro ao gerar ficha: {e}")

def app():
    st.title("🏠 Gerador de Ficha de Captação")

    secoes = {
        "Valor / Tipo de Negócio": [
            ("valor","text","Valor (R$)"), ("aluguel","checkbox","Aluguel"), ("venda","checkbox","Venda")
        ],
        "Tipo de Imóvel": [
            ("casa","checkbox","Casa"), ("Apto","checkbox","Apto"), ("Sitio","checkbox","Sítio"),
            ("lotes","checkbox","Lotes"), ("outros","checkbox","Outros")
        ],
        "Dados do Imóvel": [
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
        "Características / Infraestrutura": [
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
        "Dados do Proprietário": [
            ("nomeProprietario","text","Nome"), ("ederecoProprietario","text","Endereço"), ("numeroProprietario","text","Nº"),
            ("CompleProprietario","text","Compl"), ("bairroProprietario","text","Bairro"), ("cidadeProprietario","text","Cidade"),
            ("UFPropritario","text","UF"), ("CpfProprietario","text","CPF"), ("RGProprietario","text","RG"),
            ("emailProprietario","text","E-mail"), ("telefoneProprietario","text","Tel. Fixo"),
            ("celularProprietario","text","Celular"), ("nomeCaptador","text","Captador"),
            ("dia","text","Dia"), ("mes","text","Mês"), ("ano","text","Ano")
        ],
        "Situação das Chaves": [
            ("copiaVillares","checkbox","Cópia Villares"), ("copiaProprietario","checkbox","Cópia Proprietário")
        ]
    }

    dados_ficha = {}
    for secao, campos in secoes.items():
        with st.expander(secao, expanded=(secao=="Valor / Tipo de Negócio")):
            col_count = 3
            cols = st.columns(col_count)
            col_index = 0
            for campo, tipo, label in campos:
                key_name = campo + "_captacao"
                if tipo == "text":
                    dados_ficha[campo] = st.text_input(label, key=key_name)
                elif tipo == "checkbox":
                    dados_ficha[campo] = "✓" if cols[col_index].checkbox(label, key=key_name) else ""
                    col_index = (col_index + 1) % col_count

    if st.button("Gerar Ficha de Captação", key="gerar_ficha_captacao"):
        gerar_ficha(dados_ficha)

