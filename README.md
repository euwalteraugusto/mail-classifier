# 📧 Mail Classifier Service

Serviço **Fullstack** para classificação automática de e-mails corporativos. O sistema utiliza **IA Generativa (Llama 3.1)** para realizar uma análise semântica profunda e separar mensagens que exigem ação (produtivas) de ruídos informativos (improdutivas).

---

## 🚀 Funcionalidades

* **Inteligência Contextual:** Classificação baseada em intenção real utilizando o modelo Llama 3.1 (via Groq Cloud).
* **Saída Estruturada (JSON):** Garantia de integração entre IA e Backend através de respostas formatadas via *System Prompting*.
* **Processamento de Arquivos:** Suporte a upload de arquivos `.txt` e `.pdf` (via pdfplumber).
* **Interface Moderna:** UI responsiva construída com Tailwind CSS, incluindo estados de carregamento e feedback dinâmico de arquivos.
* **Explicabilidade:** Cada classificação é acompanhada de uma justificativa gerada pela própria IA.

---

## 🛠️ Tecnologias

* **Backend:** Python 3.9+, Flask, Groq SDK, PDFPlumber.
* **IA:** Llama 3.1-8b-instant (Modelo SOTA de baixíssima latência).
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript.
* **Segurança:** Gestão de variáveis de ambiente com `python-dotenv`.

---

## 🏗️ Estrutura do Projeto

```text
mail-classifier/
├── backend/
│   ├── app.py                 # Rotas Flask e lógica de upload
│   ├── ai_service.py          # Integração com Llama 3.1 e Prompt Engineering
│   ├── .env                   # Chaves de API (não versionado)
│   └── requirements.txt       # Dependências
└── frontend/                  # Templates e recursos estáticos

```

---

## 🔧 Configuração e Instalação

### 1. Obtenha uma Chave de API

Crie uma conta gratuita em [Groq Cloud](https://console.groq.com/) e gere sua `API_KEY`.

### 2. Instalação

```bash
# Clone o projeto
git clone https://github.com/euwalteraugusto/mail-classifier.git
cd mail-classifier/backend

# Crie o ambiente virtual e instale as dependências
python -m venv venv
source venv/bin/activate # No Windows: venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Variáveis de Ambiente

Crie um arquivo `.env` na pasta `backend/`:

```text
GROQ_API_KEY=seu_token_aqui

```

### 4. Execução

```bash
python app.py

```

Acesse: `http://localhost:5000`

---

## 📊 Fluxo de Decisão

O sistema processa a entrada (texto ou arquivo) e a submete ao motor de IA:

1. **Análise de Intenção:** O LLM avalia se a mensagem contém solicitações de ação, dúvidas técnicas, prazos ou documentos anexos.
2. **Triagem de Ruído:** Mensagens que contêm apenas saudações, confirmações simples ou notificações automáticas são marcadas como **Improdutivas**.
3. **Geração de Resposta:** O sistema sugere uma ação imediata baseada na categoria identificada.

---

## 👤 Autor

**Walter** - [LinkedIn](https://linkedin.com/in/walteraugusto) | [GitHub](https://github.com/euwalteraugusto)

---
