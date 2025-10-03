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
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute o sistema**
```bash
streamlit run dashboard.py
```


## 📁 Estrutura do Projeto
```text
villares-sistema/
├── 📄 dashboard.py              # Sistema principal
├── 📋 fichaCadastral.py         # Ficha cadastral
├── 📑 contrato.py               # Contrato de locação
├── 🏢 contratoAdministracao.py  # Contrato administrativo
├── 🔍 termo_vistoria.py         # Termo de vistoria
├── 💰 recibo.py                 # Recibo 
├── 📊 cadastroImovel.py         # Recibos em lote
├── 📁 templates/                # Templates Word
│   ├── fichaCadastral.docx
│   ├── contrato.docx
│   ├── contrato_administracao.docx
│   ├── termo_vistoria.docx
│   ├── recibo.docx
│   ├── vistoria_corrigido_dinamico.docx
│   └── Ficha_de_captacao.docx
├── 🗃️ dados.json                # Dados dos clientes
├── 🗃️ dados_vistorias.json      # Dados de vistorias
├── 👥 usuarios.json             # Usuários do sistema
├── 🖼️ villares.png              # Logo da empresa
└── 📋 requirements.txt          # Dependências do projeto
```

## 🎯 Como Usar

### Primeiro Acesso
1) Execute streamlit run dashboard.py
2) Faça login com usuário e senha
3) Navegue pelos módulos através do dashboard

### Trabalhando com Documentos
1) Busque por CPF para carregar dados existentes
2) Preencha os formulários com as informações necessárias
3) Visualize os dados antes de gerar o documento
3) Gere e baixe o documento Word (docx) finalizado

### Templates Personalizáveis
1) Todos os templates Word estão na pasta templates/
2) Personalize os layouts conforme necessidade da imobiliária
3) Mantenha as variáveis Jinja2 ({{ variavel }}) para funcionamento correto

## 🔧 Configuração

### Adicionando Usuários
Edite o arquivo usuarios.json para adicionar novos usuários:

```json
{
  "usuario": "senha",
  "admin": "123456"
}
```

### Personalizando Templates
1) Os templates usam sintaxe Jinja2 para variáveis
2) Mantenha a estrutura de tabelas e formatação
3) Teste sempre após modificações


## 📞 Suporte -Em caso de dúvidas ou problemas:

1)Verifique se todas as dependências estão instaladas
2)Confirme que os templates Word estão na pasta correta
3)Valide o formato dos arquivos JSON

## 📄 Licença
Este projeto é de uso interno da Villares Imobiliária.

## 👨‍💻 Desenvolvido por
Nícolas Lima

Sistema desenvolvido para otimizar os processos documentais da Villares Imobiliária.
