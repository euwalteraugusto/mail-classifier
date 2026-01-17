Mail Classifier Service

Serviço backend para classificação automática de emails corporativos como Produtivos ou Improdutivos, utilizando uma abordagem híbrida baseada em heurísticas semânticas, processamento de linguagem natural (NLP) e classificação zero-shot com modelos pré-treinados.

O projeto foi desenvolvido com foco em clareza arquitetural, baixa complexidade operacional e decisões explicáveis, servindo tanto como solução funcional quanto como material de estudo.

🎯 Objetivo do Projeto

Demonstrar uma arquitetura simples, extensível e segura para classificação de emails, priorizando:

Alta taxa de assertividade

Baixo acoplamento entre regras e modelo

Redução de falsos negativos críticos

Facilidade de evolução futura

Decisões de classificação explicáveis

Este projeto não depende de dataset próprio nem de treinamento supervisionado, tornando-o ideal para cenários iniciais ou provas de conceito.

🧠 Estratégia de Classificação

A classificação segue um pipeline híbrido em camadas, onde cada etapa tem uma responsabilidade clara:

1. Heurísticas Semânticas (Fast Path)

Aplicadas antes do uso do modelo de NLP, para lidar com casos óbvios:

Emails muito curtos

Mensagens puramente cordiais

Confirmações simples sem solicitação implícita

Essas regras:

Reduzem custo computacional

Aumentam previsibilidade

Evitam overfitting semântico do modelo

2. Classificação Zero-Shot (Core NLP)

Para mensagens não resolvidas pelas heurísticas, é utilizado o modelo:

facebook/bart-large-mnli

Características:

Zero-shot classification (não requer treino adicional)

Avalia hipóteses semânticas completas

Boa capacidade de generalização para textos corporativos

Exemplo de hipótese utilizada:

“Este email é Produtivo e requer ação, resposta, análise ou tomada de decisão.”

3. Threshold de Confiança + Fallback Seguro

Após a inferência:

Se a confiança do modelo for baixa, o sistema assume Produtivo

Essa decisão é intencional e conservadora

Motivação:

Em ambientes corporativos, perder um email relevante é mais crítico do que responder algo desnecessário

🏗️ Arquitetura do Sistema
mail-classifier/
├── backend/
│   ├── app.py              # API Flask (ponto de entrada)
│   ├── ai_service.py       # Lógica de classificação e geração de resposta
│   ├── nlp_utils.py        # Utilitários NLP (normalização, lematização, etc.)
│   ├── requirements.txt    # Dependências do backend
│   ├── examples/           # Exemplos de emails para teste
│   └── README.md           # Documentação específica do backend
│
├── frontend/
│   ├── templates/
│   │   └── index.html      # Interface web simples
│   └── static/
│       ├── styles.css
│       └── ui.js
│
├── .gitignore
└── README.md               # Documentação principal

🔧 Tecnologias Utilizadas
Backend

Python 3

Flask

Transformers (Hugging Face)

NLTK

BART MNLI (facebook/bart-large-mnli)

Frontend

HTML

CSS

JavaScript (fetch API)

▶️ Como Executar o Projeto
1. Clonar o repositório
git clone https://github.com/euwalteraugusto/mail-classifier.git
cd mail-classifier

2. Criar e ativar ambiente virtual
python -m venv venv


Windows

venv\Scripts\activate


Linux / macOS

source venv/bin/activate

3. Instalar dependências
pip install -r backend/requirements.txt

4. Executar o servidor
python backend/app.py


A aplicação estará disponível em:

http://127.0.0.1:5000

📌 Exemplo de Uso

Entrada:

"Algum retorno referente ao arquivo que enviamos anteriormente?"


Classificação esperada:

Produtivo

⚠️ Limitações Conhecidas

Classificação baseada apenas em conteúdo textual

Modelo não foi ajustado com dados específicos do domínio

Linguagem informal ou ambígua pode gerar falsos positivos

Não há persistência de histórico ou métricas

Essas limitações são conscientes e fazem parte da proposta didática do projeto.

🚀 Possíveis Evoluções

Cache de inferências

Métricas de confiança expostas via API

Logs explicáveis por decisão

Ajuste dinâmico de threshold

Integração com serviços de email reais

Fine-tuning supervisionado opcional

👤 Autor

Walter Augusto
Estudante e desenvolvedor em formação, com foco em engenharia de software, automação e sistemas inteligentes.
