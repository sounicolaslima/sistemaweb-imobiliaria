import streamlit as st
from docxtpl import DocxTemplate
import os
from datetime import datetime
from io import BytesIO

# ----------------- Caminhos dos templates -----------------
base_dir = os.path.dirname(__file__)
TEMPLATE_UNICO = os.path.join(base_dir, "recibo_unico.docx")
TEMPLATE_DUPLO = os.path.join(base_dir, "recibo_duplo.docx")

def gerar_recibos(recibos):
    """Gera documento com recibos usando templates apropriados"""
    try:
        # Verificar templates
        if not os.path.exists(TEMPLATE_UNICO):
            st.error(f"Template {TEMPLATE_UNICO} não encontrado.")
            return None
        if not os.path.exists(TEMPLATE_DUPLO):
            st.error(f"Template {TEMPLATE_DUPLO} não encontrado.")
            return None

        # Para um único recibo
        if len(recibos) == 1:
            doc = DocxTemplate(TEMPLATE_UNICO)
            dados = {**recibos[0], 'valorTotal': calcular_total(recibos[0])}
            doc.render(dados)
        else:
            # Para múltiplos recibos - usar template duplo
            doc = DocxTemplate(TEMPLATE_DUPLO)
            dados_template = {}
            
            # Processar cada recibo
            for i, recibo in enumerate(recibos[:2]):  # Máximo 2 por página
                sufixo = "" if i == 0 else "2"
                for key, value in recibo.items():
                    dados_template[f"{key}{sufixo}"] = value
                dados_template[f"valorTotal{sufixo}"] = calcular_total(recibo)
            
            doc.render(dados_template)

        # Salvar em memória
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return buffer

    except Exception as e:
        st.error(f"Erro ao gerar recibos: {e}")
        return None

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

def app():
    from theme import apply_theme
    apply_theme()

    st.set_page_config(page_title="Recibo de Aluguel", page_icon="🏠", layout="centered")
    
    st.title("📄 Recibo de Aluguel - Villares Imóveis")

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Inicializar lista de recibos
    if 'recibos' not in st.session_state:
        st.session_state.recibos = []

    # Verificação dos templates
    templates_ok = True
    if not os.path.exists(TEMPLATE_UNICO):
        st.error(f"❌ {TEMPLATE_UNICO} não encontrado")
        templates_ok = False
    if not os.path.exists(TEMPLATE_DUPLO):
        st.error(f"❌ {TEMPLATE_DUPLO} não encontrado")
        templates_ok = False
    
    if templates_ok:
        st.success("✅ Templates encontrados!")

    # Formulário principal
    with st.form("recibo_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nomeLocatario = st.text_input("Locatário(a):")
            enderecoImovel = st.text_input("Endereço do Imóvel:")
            inicioPeriodo = st.text_input("Período de:")
            finalPeriodo = st.text_input("Até:")
            vencimento = st.text_input("Vencimento:")
            limitePagamento = st.text_input("Limite Pagamento:")
        
        with col2:
            valorAluguel = st.text_input("Valor Aluguel:", value="0,00")
            valorAgua = st.text_input("Valor Água:", value="0,00")
            valorLuz = st.text_input("Valor Luz:", value="0,00")
            valorIPTU = st.text_input("Valor IPTU:", value="0,00")
            valorCondominio = st.text_input("Valor Condomínio:", value="0,00")
            valorMulta = st.text_input("Valor Multa:", value="0,00")
            desconto = st.text_input("Desconto:", value="0,00")
            data = st.text_input("Data:", value=datetime.now().strftime('%d/%m/%Y'))
        
        submitted = st.form_submit_button("➕ Adicionar Recibo")

        if submitted and templates_ok:
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
            st.session_state.recibos.append(recibo)
            st.success(f"Recibo adicionado! Total: {len(st.session_state.recibos)}")

    # Lista de recibos
    if st.session_state.recibos:
        st.subheader(f"📋 Recibos Adicionados ({len(st.session_state.recibos)})")
        
        for i, recibo in enumerate(st.session_state.recibos):
            with st.expander(f"Recibo {i+1} - {recibo.get('nomeLocatario', 'Sem nome')}"):
                st.write(f"**Endereço:** {recibo.get('enderecoImovel', 'Não informado')}")
                st.write(f"**Período:** {recibo.get('inicioPeriodo', '')} a {recibo.get('finalPeriodo', '')}")
                st.write(f"**Total:** R$ {calcular_total(recibo)}")
                
                if st.button(f"🗑️ Remover Recibo {i+1}", key=f"remove_{i}"):
                    st.session_state.recibos.pop(i)
                    st.rerun()

        # Botão de geração
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Gerar Documento", type="primary", use_container_width=True):
                with st.spinner("Gerando recibos..."):
                    buffer = gerar_recibos(st.session_state.recibos)
                    
                    if buffer:
                        st.success("✅ Documento gerado com sucesso!")
                        
                        nome_arquivo = f"recibos_{datetime.now().strftime('%Y%m%d_%H%M')}.docx"
                        
                        st.download_button(
                            label="📥 Baixar Recibos",
                            data=buffer,
                            file_name=nome_arquivo,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            type="primary"
                        )
        
        with col2:
            if st.button("🗑️ Limpar Tudo", use_container_width=True):
                st.session_state.recibos = []
                st.rerun()

    # Instruções
    st.markdown("---")
    st.info("""
    💡 **Como usar:**
    1. Preencha os dados do recibo
    2. Clique em **Adicionar Recibo** para incluir na lista
    3. Repita para adicionar mais recibos (máximo 2 por documento)
    4. Clique em **Gerar Documento** para criar o arquivo Word
    5. **Layout automático:**
       - 1 recibo → Template único
       - 2 recibos → Template duplo (2 por página)
    """)
st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    app()