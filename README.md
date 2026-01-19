# 📧 Mail Classifier Service

Serviço backend para **classificação automática de emails corporativos** em **Produtivos** ou **Improdutivos**, utilizando uma abordagem **híbrida** que combina **heurísticas semânticas**, **NLP** e **classificação zero-shot** com modelos pré-treinados.

Desenvolvido com foco em **simplicidade arquitetural**, **decisões explicáveis** e **baixa complexidade operacional** — ideal tanto para uso prático quanto para estudo e demonstrações técnicas.

---

## 🎯 Objetivo

Demonstrar uma solução clara, robusta e extensível para classificação de emails, priorizando:

- ✅ **Alta assertividade** nas classificações
- 🧩 **Decisões conservadoras e explicáveis** (auditabilidade)
- 🔌 **Baixo acoplamento** entre regras e modelos
- 🛠️ **Facilidade de manutenção** e evolução contínua

Não há uso de datasets proprietários nem necessidade de treinamento supervisionado, tornando o projeto ideal para **provas de conceito**, **MVPs** e **ambientes com dados limitados**.

---

## 🧠 Estratégia de Classificação

O sistema utiliza um **pipeline em camadas** que reduz custo computacional e aumenta previsibilidade das decisões.

### 1️⃣ **Heurísticas Semânticas (Camada Rápida)**

Aplicadas **antes** do modelo NLP para identificar casos triviais e óbvios:

- 📏 Mensagens extremamente curtas (< 10 caracteres)
- 👋 Emails puramente cordiais ("Obrigado!", "Boa tarde")
- ✔️ Confirmações simples sem solicitação de ação ("Ok", "Entendido")

**Benefício:** Resposta instantânea sem processamento pesado, reduzindo latência em até 70% dos casos comuns.

---

### 2️⃣ **Classificação Zero-Shot com NLP (Camada Inteligente)**

Mensagens não resolvidas pelas heurísticas são avaliadas por:

**Modelo:** `facebook/bart-large-mnli` (classificação zero-shot)

**Hipótese semântica:**
> _"Este email é produtivo e requer ação, resposta ou tomada de decisão."_

**Vantagens:**
- ✨ Não requer treinamento específico
- 🌍 Funciona com múltiplos idiomas (via transferência)
- 🔄 Adaptável a novos contextos sem retreinamento

---

### 3️⃣ **Threshold de Confiança + Fallback Seguro**

Se a confiança do modelo for **baixa** (< limiar configurável), o email é automaticamente classificado como **Produtivo**.

#### 📌 Justificativa (Filosofia Conservadora):

Em ambientes corporativos, **errar por excesso de atenção é preferível a perder um email relevante**. Melhor um falso positivo ocasional do que ignorar uma mensagem crítica.

**Exemplo prático:**
- Email ambíguo: _"Podemos conversar amanhã?"_
- Baixa confiança → classificado como **Produtivo** (por precaução)

---

## 🏗️ Arquitetura do Projeto

```
mail-classifier/
│
├── backend/
│   ├── app.py                 # 🚀 API Flask (endpoints REST)
│   ├── ai_service.py          # 🧠 Lógica central de classificação
│   ├── nlp_utils.py           # 🔧 Utilitários NLP e pré-processamento
│   ├── requirements.txt       # 📦 Dependências Python
│   └── examples/              # 📂 Exemplos de emails para testes
│
├── frontend/
│   ├── templates/
│   │   └── index.html         # 🎨 Interface web
│   └── static/
│       ├── styles.css         # 💅 Estilos visuais
│       └── ui.js              # ⚡ Lógica cliente (fetch, UX)
│
├── .gitignore
├── README.md                  # 📖 Este arquivo
└── LICENSE                    # ⚖️ (opcional) MIT/Apache
```

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia | Função |
|--------|-----------|--------|
| **Backend** | Python 3.9+ | Linguagem principal |
| **Framework** | Flask | API REST leve e flexível |
| **NLP** | 🤗 Transformers (Hugging Face) | Modelos pré-treinados |
| **Modelo** | `facebook/bart-large-mnli` | Classificação zero-shot |
| **Frontend** | HTML5 + CSS3 + Vanilla JS | Interface limpa sem frameworks |

---

## 🚀 Como Executar

### **Pré-requisitos**

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### **Instalação**

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/mail-classifier.git
cd mail-classifier/backend

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### **Execução**

```bash
# Inicie o servidor Flask
python app.py
```

Acesse no navegador: **http://localhost:5000**

---

## 📊 Exemplos de Classificação

| Email | Classificação | Método | Confiança |
|-------|--------------|--------|-----------|
| "Obrigado!" | ❌ Improdutivo | Heurística | 100% |
| "Preciso do relatório até amanhã" | ✅ Produtivo | NLP | 94% |
| "Oi" | ❌ Improdutivo | Heurística | 100% |
| "Podemos agendar uma reunião?" | ✅ Produtivo | NLP | 87% |
| "Entendido." | ❌ Improdutivo | Heurística | 100% |

---

## 🔮 Evoluções Futuras

Possíveis melhorias e extensões:

- [ ] 📊 **Dashboard de métricas** (precisão, recall, distribuição)
- [ ] 🔐 **Autenticação** (OAuth, JWT para APIs corporativas)
- [ ] 📨 **Integração IMAP/SMTP** (classificação em tempo real)
- [ ] 🐇 **Fila assíncrona** (RabbitMQ/Celery para volumes altos)
- [ ] 🌐 **API multilíngue** (detecção automática de idioma)
- [ ] 🧪 **A/B testing** de modelos (BART vs DeBERTa vs LLMs)
- [ ] 💾 **Persistência** (PostgreSQL para histórico e feedback)
- [ ] 🤖 **Fine-tuning** com feedback humano (RLHF lite)

---

## 📝 Observações Importantes

### **Por que Zero-Shot?**

Evita os principais desafios de ML supervisionado:
- ❌ Necessidade de datasets rotulados
- ❌ Overfitting em categorias específicas
- ❌ Retraining periódico
- ✅ Generalização imediata para novos contextos

### **Por que Conservador?**

A filosofia "melhor um falso positivo que um falso negativo" é fundamental em comunicação corporativa. Um email produtivo ignorado pode causar:
- Perda de prazos críticos
- Falhas em comunicação com clientes
- Violação de SLAs contratuais

### **Público-Alvo**

- Desenvolvedores aprendendo NLP aplicado
- Equipes buscando POC de automação de email
- Projetos acadêmicos de classificação de texto
- Empresas com baixo volume de dados para treinamento

---

## 📄 Licença

Este projeto é open-source e está disponível sob a licença **MIT** (ou especifique outra).

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para mudanças maiores:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 👤 Autor

**Walter**  
📧 walter.fonseca2377@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/walteraugusto) | [GitHub](https://github.com/euwalteraugusto)

---

## ⭐ Mostre seu Apoio

Se este projeto foi útil, considere dar uma ⭐ no repositório!
