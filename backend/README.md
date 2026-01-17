# 📧 Mail Classifier Service

Serviço backend para **classificação automática de emails corporativos** como **Produtivos** ou **Improdutivos**, utilizando uma abordagem **híbrida** baseada em **heurísticas semânticas**, **processamento de linguagem natural (NLP)** e **classificação zero-shot** com modelos pré-treinados.

Projeto desenvolvido com foco em **clareza arquitetural**, **baixa complexidade operacional** e **decisões explicáveis**, servindo tanto como solução funcional quanto como material de estudo.

---

## 🎯 Objetivo do Projeto

Demonstrar uma arquitetura simples, extensível e segura para classificação de emails, priorizando:

- ✅ Alta taxa de assertividade  
- 🔗 Baixo acoplamento entre regras e modelo  
- 🧠 Decisões explicáveis  
- 🛡️ Redução de falsos negativos críticos  
- 🔄 Facilidade de evolução futura  

O projeto **não depende de dataset próprio** nem de treinamento supervisionado, sendo ideal para provas de conceito e estudos arquiteturais.

---

## 🧠 Estratégia de Classificação

A classificação segue um **pipeline híbrido em camadas**, onde cada etapa tem uma responsabilidade clara.

### 1️⃣ Heurísticas Semânticas (Fast Path)

Aplicadas antes do uso de modelos NLP, para resolver casos óbvios:

- Emails muito curtos  
- Mensagens puramente cordiais  
- Confirmações simples sem solicitação implícita  

Benefícios:

- Redução de custo computacional  
- Maior previsibilidade  
- Menor dependência do modelo  

---

### 2️⃣ Classificação Zero-Shot (Core NLP)

Para mensagens não resolvidas pelas heurísticas, utiliza-se o modelo:

- **facebook/bart-large-mnli**

Características:

- Zero-shot classification (dispensa treinamento)  
- Avaliação semântica baseada em hipóteses  
- Boa generalização para linguagem corporativa  

Hipótese utilizada:

> _"Este email é **Produtivo** e requer ação, resposta, análise ou tomada de decisão."_

---

### 3️⃣ Threshold de Confiança + Fallback Seguro

Após a inferência:

- Caso a **confiança do modelo seja baixa**, o sistema assume **Produtivo**
- Decisão **intencionalmente conservadora**

📌 **Motivação:**  
Em ambientes corporativos, **perder um email relevante é mais crítico** do que responder algo irrelevante.

---

## 🏗️ Arquitetura do Sistema

```text
mail-classifier/
├── backend/
│   ├── app.py              # API Flask (ponto de entrada)
│   ├── ai_service.py       # Classificação e geração de resposta
│   ├── nlp_utils.py        # Utilitários NLP
│   ├── requirements.txt    # Dependências do backend
│   ├── examples/           # Exemplos de emails
│   └── README.md           # Documentação do backend
│
├── frontend/
│   ├── templates/
│   │   └── index.html      # Interface web
│   └── static/
│       ├── styles.css
│       └── ui.js
│
├── .gitignore
└── README.md
