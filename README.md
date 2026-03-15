# 📧 Mail Classifier Service

Serviço **Fullstack** para classificação automática de e-mails corporativos. O sistema utiliza um pipeline híbrido que combina **IA Generativa (Llama 3.1)** e heurísticas para separar mensagens produtivas de ruídos informativos.

---

## 🚀 Funcionalidades

- **Classificação Híbrida:** Integração com LLM de última geração (Llama 3.1 via Groq) para análise de intenção.
- **Processamento de Arquivos:** Suporte a upload de arquivos `.txt` e `.pdf` (via pdfplumber).
- **Interface Moderna:** UI responsiva construída com Tailwind CSS, incluindo feedbacks de carregamento e seleção de arquivos.
- **Explicabilidade:** Cada decisão da IA é acompanhada de uma justificativa (`source`) exibida na interface.

---

## 🛠️ Tecnologias

- **Backend:** Python 3.9+, Flask, Groq SDK, PDFPlumber.
- **IA:** Llama 3.1-8b-instant (Modelo SOTA de baixa latência).
- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript.
- **Segurança:** Gestão de variáveis de ambiente com `python-dotenv`.

---

## 🏗️ Estrutura do Projeto

```text
mail-classifier/
├── backend/
│   ├── app.py                 # Rotas Flask e lógica de upload
│   ├── ai_service.py          # Integração com Llama 3.1 e Prompt Engineering
│   ├── nlp_utils.py           # Utilitários de limpeza de texto
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
git clone [https://github.com/euwalteraugusto/mail-classifier.git](https://github.com/euwalteraugusto/mail-classifier.git)
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

## 📊 Pipeline de Decisão

O sistema analisa o e-mail em dois níveis:

1. **Heurística:** Filtra mensagens triviais ou curtas demais para economizar tokens e latência.
2. **LLM (Llama 3.1):** Realiza a interpretação semântica profunda da mensagem, identificando se há necessidade de ação (Produtivo) ou se é apenas informativo/saudação (Improdutivo).

---

## 👤 Autor

**Walter** - [LinkedIn](https://linkedin.com/in/walteraugusto) | [GitHub](https://github.com/euwalteraugusto)

```

---
