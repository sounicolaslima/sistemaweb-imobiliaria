import streamlit as st
from docxtpl import DocxTemplate
import os
from datetime import datetime
from io import BytesIO

# ----------------- Caminhos dos templates -----------------
base_dir = os.path.dirname(__file__)
TEMPLATE_RECIBO = os.path.join(base_dir, "recibo.docx")

def calcular_total(recibo):
    """Calcula o total do recibo"""
    try:
        total = (float(recibo.get('valorAluguel', '0').replace(',', '.')) +
                float(recibo.get('valorAgua', '0').replace(',', '.')) +
                float(recibo.get('valorLuz', '0').replace(',', '.')) +
                float(recibo.get('valorIPTU', '0').replace(',', '.')) +
                float(recibo.get('valorCondominio', '0').replace(',', '.')) +
                float(recibo.get('valorMulta', '0').replace(',', '.')) -
                float(recibo.get('desconto', '0').replace(',', '.')))
        return f"{total:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')
    except:
        return '0,00'

def gerar_recibo(dados):
    """Gera um único recibo"""
    try:
        # Verificar template
        if not os.path.exists(TEMPLATE_RECIBO):
            st.error(f"Template {TEMPLATE_RECIBO} não encontrado.")
            return None

        # Carregar e renderizar o template
        doc = DocxTemplate(TEMPLATE_RECIBO)
        
        dados_template = {
            'nomeLocatario': dados.get('nomeLocatario', ''),
            'enderecoImovel': dados.get('enderecoImovel', ''),
            'inicioPeríodo': dados.get('inicioPeriodo', ''),
            'finalPeríodo': dados.get('finalPeriodo', ''),
            'vencimento': dados.get('vencimento', ''),
            'limitePagamento': dados.get('limitePagamento', ''),
            'valorAluguel': dados.get('valorAluguel', '0,00'),
            'valorAgua': dados.get('valorAgua', '0,00'),
            'valorLuz': dados.get('valorLuz', '0,00'),
            'valorIPTU': dados.get('valorIPTU', '0,00'),
            'valorCondominio': dados.get('valorCondominio', '0,00'),
            'valorMulta': dados.get('valorMulta', '0,00'),
            'desconto': dados.get('desconto', '0,00'),
            'data': dados.get('data', ''),
            'valorTotal': calcular_total(dados)
        }
        
        doc.render(dados_template)

        # Salvar em memória
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return buffer

    except Exception as e:
        st.error(f"Erro ao gerar recibo: {e}")
        return None

def app():
    from theme import apply_theme
    apply_theme()

    st.set_page_config(page_title="Recibo de Aluguel", page_icon="🏠", layout="centered")
    
    # CORREÇÃO: Botão voltar no topo + compatibilidade
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "inicial"

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ VOLTAR", use_container_width=True):
            st.session_state.pagina = "inicial"
            st.rerun()
    with col_title:
        st.title("📄 Recibo de Aluguel")

    # Verificação do template
    if not os.path.exists(TEMPLATE_RECIBO):
        st.error(f"❌ {TEMPLATE_RECIBO} não encontrado")
        st.info("""
        **Por favor verifique:**
        1. O arquivo 'recibo.docx' está na mesma pasta do script
        2. O nome do arquivo está correto
        3. O arquivo não está corrompido
        """)
    else:
        st.success("✅ Template encontrado!")

    # Formulário principal
    with st.form("recibo_form"):
        st.subheader("📝 Dados do Recibo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nomeLocatario = st.text_input("Locatário(a):", placeholder="Nome completo do locatário")
            inicioPeriodo = st.text_input("Período de:", placeholder="dd/mm/aaaa")
            vencimento = st.text_input("Vencimento:", placeholder="dd/mm/aaaa")
            valorAluguel = st.text_input("Valor Aluguel (R$):", value="0,00")
            valorLuz = st.text_input("Valor Luz (R$):", value="0,00")
            valorCondominio = st.text_input("Valor Condomínio (R$):", value="0,00")
            data = st.text_input("Data do Recibo:", value=datetime.now().strftime('%d/%m/%Y'))
            
        with col2:
            enderecoImovel = st.text_input("Endereço do Imóvel:", placeholder="Endereço completo do imóvel")
            finalPeriodo = st.text_input("Até:", placeholder="dd/mm/aaaa")
            limitePagamento = st.text_input("Limite Pagamento:", placeholder="dd/mm/aaaa")
            valorAgua = st.text_input("Valor Água (R$):", value="0,00")
            valorIPTU = st.text_input("Valor IPTU (R$):", value="0,00")
            valorMulta = st.text_input("Valor Multa (R$):", value="0,00")
            desconto = st.text_input("Desconto (R$):", value="0,00")
        
        # Botões do formulário
        col1, col2 = st.columns(2)
        with col1:
            visualizar = st.form_submit_button("👁️ Visualizar Recibo", use_container_width=True)
        with col2:
            gerar = st.form_submit_button("🔄 Gerar Recibo", type="primary", use_container_width=True)

    # Processar visualização do recibo
    if visualizar and os.path.exists(TEMPLATE_RECIBO):
        recibo = {
            'nomeLocatario': nomeLocatario,
            'enderecoImovel': enderecoImovel,
            'inicioPeriodo': inicioPeriodo,
            'finalPeriodo': finalPeriodo,
            'vencimento': vencimento,
            'limitePagamento': limitePagamento,
            'valorAluguel': valorAluguel,
            'valorAgua': valorAgua,
            'valorLuz': valorLuz,
            'valorIPTU': valorIPTU,
            'valorCondominio': valorCondominio,
            'valorMulta': valorMulta,
            'desconto': desconto,
            'data': data
        }
        
        st.subheader("👀 Visualização do Recibo")
        
        # Mostrar resumo detalhado
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Dados do Recibo:**")
            st.write(f"**Locatário:** {nomeLocatario or 'Não informado'}")
            st.write(f"**Endereço:** {enderecoImovel or 'Não informado'}")
            st.write(f"**Período:** {inicioPeriodo or 'Não informado'} a {finalPeriodo or 'Não informado'}")
            st.write(f"**Vencimento:** {vencimento or 'Não informado'}")
            st.write(f"**Limite Pag.:** {limitePagamento or 'Não informado'}")
            st.write(f"**Data Recibo:** {data or 'Não informado'}")
        
        with col2:
            st.write("**Valores:**")
            st.write(f"**Aluguel:** R$ {valorAluguel or '0,00'}")
            st.write(f"**Água:** R$ {valorAgua or '0,00'}")
            st.write(f"**Luz:** R$ {valorLuz or '0,00'}")
            st.write(f"**IPTU:** R$ {valorIPTU or '0,00'}")
            st.write(f"**Condomínio:** R$ {valorCondominio or '0,00'}")
            st.write(f"**Multa:** R$ {valorMulta or '0,00'}")
            st.write(f"**Desconto:** R$ {desconto or '0,00'}")
            st.success(f"**TOTAL: R$ {calcular_total(recibo)}**")
        
        st.info("💡 **Verifique os dados acima. Se estiverem corretos, clique em 'Gerar Recibo' para criar o arquivo Word.**")

    # Processar geração do recibo
    if gerar and os.path.exists(TEMPLATE_RECIBO):
        recibo = {
            'nomeLocatario': nomeLocatario,
            'enderecoImovel': enderecoImovel,
            'inicioPeriodo': inicioPeriodo,
            'finalPeriodo': finalPeriodo,
            'vencimento': vencimento,
            'limitePagamento': limitePagamento,
            'valorAluguel': valorAluguel,
            'valorAgua': valorAgua,
            'valorLuz': valorLuz,
            'valorIPTU': valorIPTU,
            'valorCondominio': valorCondominio,
            'valorMulta': valorMulta,
            'desconto': desconto,
            'data': data
        }
        
        with st.spinner("Gerando recibo..."):
            buffer = gerar_recibo(recibo)
            
            if buffer:
                st.success("✅ Recibo gerado com sucesso!")
                
                # Criar nome do arquivo
                nome_locatario = nomeLocatario.replace(" ", "_") if nomeLocatario else "recibo"
                nome_arquivo = f"Recibo_{nome_locatario}_{datetime.now().strftime('%Y%m%d_%H%M')}.docx"
                
                # Botão de download
                st.download_button(
                    label="📥 Baixar Recibo",
                    data=buffer,
                    file_name=nome_arquivo,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="primary",
                    use_container_width=True
                )

    # Instruções
    st.markdown("---")
    st.info("""
    💡 **Como usar:**
    1. Preencha todos os dados do recibo no formulário
    2. Clique em **👁️ Visualizar Recibo** para verificar os dados antes de gerar
    3. Clique em **🔄 Gerar Recibo** para criar o arquivo Word
    4. Clique em **📥 Baixar Recibo** para salvar o arquivo
    5. Imprima o recibo gerado
    
    """)
    
    # CORREÇÃO: REMOVIDO o fechamento do container
    # st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    app()
    