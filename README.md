# 🏢 Sistema Villares Imobiliária

Sistema completo de gestão imobiliária desenvolvido em Streamlit para automação de documentos e processos administrativos.

## 🚀 Funcionalidades

### 📋 Módulos do Sistema

| Módulo | Descrição |
|--------|-----------|
| **🏠 Dashboard Principal** | Sistema centralizado com autenticação e navegação |
| **👤 Ficha Cadastral** | Cadastro completo de locatários e fiadores |
| **📑 Contrato de Locação** | Geração de contratos de aluguel padrão |
| **🏢 Contrato de Administração** | Contratos para administração de imóveis |
| **🔍 Termo de Vistoria** | Vistoria detalhada com cômodos e características |
| **💰 Recibo de Aluguel** | Emissão de recibos individuais |
| **📊 Recibos Múltiplos** | Sistema de recibos em lote (até 2 por página) |

### ✨ Características Técnicas

- **🖥️ Interface Moderna**: Dashboard responsivo com design profissional
- **🔐 Sistema de Login**: Autenticação segura com usuários em JSON
- **📄 Geração de Documentos**: Templates Word personalizáveis
- **💾 Persistência de Dados**: Armazenamento em JSON para reutilização
- **🔍 Busca Inteligente**: Localização por CPF para dados existentes
- **🎨 Formatação Avançada**: RichText para documentos profissionais
- **🧮 Cálculos Automáticos**: Totais, valores e períodos automáticos
- **📱 Design Responsivo**: CSS personalizado para melhor experiência

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Framework web
- **python-docx-template** - Geração de documentos Word
- **PIL (Pillow)** - Manipulação de imagens
- **JSON** - Armazenamento de dados
- **Requests** - Integração com APIs

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/villares-sistema.git
cd villares-sistema
Crie um ambiente virtual (recomendado)

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
Instale as dependências

bash
pip install -r requirements.txt
Execute o sistema

bash
streamlit run dashboard.py
📁 Estrutura do Projeto
text
villares-sistema/
├── 📄 dashboard.py              # Sistema principal
├── 📋 fichaCadastral.py         # Ficha cadastral
├── 📑 contrato.py               # Contrato de locação
├── 🏢 contratoAdministracao.py  # Contrato administrativo
├── 🔍 termo_vistoria.py         # Termo de vistoria
├── 💰 recibo.py                 # Recibo individual
├── 📊 recibo_multiplo.py        # Recibos em lote
├── 📁 templates/                # Templates Word
│   ├── fichaCadastral.docx
│   ├── contrato.docx
│   ├── contrato_administracao.docx
│   ├── termo_vistoria.docx
│   ├── recibo.docx
│   ├── recibo_unico.docx
│   └── recibo_duplo.docx
├── 🗃️ dados.json                # Dados dos clientes
├── 🗃️ dados_vistorias.json     # Dados de vistorias
├── 👥 usuarios.json             # Usuários do sistema
├── 🖼️ villares.png              # Logo da empresa
└── 📋 requirements.txt          # Dependências do projeto
🎯 Como Usar
Primeiro Acesso
Execute streamlit run dashboard.py

Faça login com usuário e senha

Navegue pelos módulos através do dashboard

Trabalhando com Documentos
Busque por CPF para carregar dados existentes

Preencha os formulários com as informações necessárias

Visualize os dados antes de gerar o documento

Gere e baixe o documento Word finalizado

Templates Personalizáveis
Todos os templates Word estão na pasta templates/

Personalize os layouts conforme necessidade da imobiliária

Mantenha as variáveis Jinja2 ({{ variavel }}) para funcionamento correto

🔧 Configuração
Adicionando Usuários
Edite o arquivo usuarios.json para adicionar novos usuários:

json
{
  "usuario": "senha",
  "admin": "123456"
}
Personalizando Templates
Os templates usam sintaxe Jinja2 para variáveis

Mantenha a estrutura de tabelas e formatação

Teste sempre após modificações

📞 Suporte
Em caso de dúvidas ou problemas:

Verifique se todas as dependências estão instaladas

Confirme que os templates Word estão na pasta correta

Valide o formato dos arquivos JSON

📄 Licença
Este projeto é de uso interno da Villares Imobiliária.

👨‍💻 Desenvolvido por
Nícolas Lima

Sistema desenvolvido para otimizar os processos documentais da Villares Imobiliária.
