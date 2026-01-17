from transformers import pipeline

# Lista de labels (rótulos) utilizadas para classificação de emails.
# Explícito para manutenção futura.
LABELS = ["Produtivo", "Improdutivo"]

# Criamos um pipeline de classificação zero-shot usando o modelo "facebook/bart-large-mnli".
# O zero-shot é escolhido porque permite classificar textos em categorias sem necessidade de treino adicional.
# Modelo gratuito e robusto para tarefas de classificação sem dataset específico.
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Criação de um pipeline de geração de texto usando o modelo "gpt2".
# O GPT-2 é usado apenas como exemplo de geração de texto simples e gratuito.
# Em produção, poderíamos considerar modelos mais avançados.
generator = pipeline(
    "text-generation",
    model="gpt2"
)


def classify_email(text):
    """
    Classifica um email como 'Produtivo' ou 'Improdutivo'.

    Definição operacional adotada neste serviço:
    - Email PRODUTIVO: qualquer mensagem que exija resposta humana,
      ação, acompanhamento ou tomada de decisão, ainda que de forma implícita.
    - Email IMPRODUTIVO: mensagens puramente cordiais, informativas
      ou que não demandem resposta.

    A estratégia de classificação segue uma abordagem híbrida:
    1. Heurísticas semânticas de alta precisão (baixo custo e alto impacto).
    2. Classificação zero-shot com modelo BART (quando necessário).
    3. Fallback seguro para evitar falsos negativos críticos.

    Args:
        text (str): Conteúdo textual do email.

    Returns:
        str: 'Produtivo' ou 'Improdutivo'.
    """

    # ------------------------------------------------------------------
    # Normalização básica
    # ------------------------------------------------------------------
    # Normalizamos o texto apenas para comparações internas.
    # O texto original é preservado para o modelo.
    normalized_text = text.strip().lower()

    # ------------------------------------------------------------------
    # Heurística 1: Mensagens muito curtas
    # ------------------------------------------------------------------
    # Emails extremamente curtos tendem a ser confirmações ou cordialidades.
    if len(normalized_text) < 20:
        return "Improdutivo"

    # ------------------------------------------------------------------
    # Heurística 2: Mensagens puramente cordiais
    # ------------------------------------------------------------------
    # Lista intencionalmente restrita para evitar falsos positivos.
    cordial_expressions = [
        "obrigado",
        "obrigada",
        "ok",
        "ciente",
        "entendido",
        "bom dia",
        "boa tarde",
        "boa noite"
    ]

    # Se o email for apenas uma cordialidade ou começar com ela,
    # assumimos que não há demanda de resposta.
    if any(
        normalized_text == expr or normalized_text.startswith(expr + " ")
        for expr in cordial_expressions
    ):
        return "Improdutivo"

    # ------------------------------------------------------------------
    # Heurística 3 (CRÍTICA): Intenção implícita de resposta humana
    # ------------------------------------------------------------------
    # Esta é a principal alavanca de assertividade do sistema.
    # Perguntas profissionais, follow-ups e cobranças educadas
    # quase sempre exigem resposta, mesmo sem verbos imperativos.
    response_intent_indicators = [
        "algum retorno",
        "aguardamos retorno",
        "aguardo retorno",
        "poderia informar",
        "poderiam informar",
        "poderia verificar",
        "poderiam verificar",
        "status",
        "atualização",
        "posicionamento",
        "referente ao",
        "referente a",
        "conforme enviado",
        "enviado anteriormente",
        "mensagem anterior",
        "arquivo enviado",
        "ficamos no aguardo",
        "aguardamos"
    ]

    # Presença de interrogação é um forte sinal de expectativa de resposta.
    has_question_mark = "?" in normalized_text

    # Caso qualquer um dos sinais apareça, classificamos diretamente
    # como produtivo, evitando depender do modelo zero-shot.
    if has_question_mark or any(
        indicator in normalized_text
        for indicator in response_intent_indicators
    ):
        return "Produtivo"

    # ------------------------------------------------------------------
    # Classificação zero-shot (quando heurísticas não são suficientes)
    # ------------------------------------------------------------------
    # Aqui delegamos ao modelo apenas os casos ambíguos,
    # reduzindo erros confiantes e custo computacional.
    result = classifier(
        text,
        candidate_labels=LABELS,
        hypothesis_template=(
            "Este email é {} e requer ação, resposta, análise ou tomada de decisão."
        )
    )

    # O pipeline retorna os rótulos ordenados por probabilidade.
    label = result["labels"][0]
    score = result["scores"][0]

    # ------------------------------------------------------------------
    # Fallback de segurança
    # ------------------------------------------------------------------
    # Em cenários de baixa confiança, optamos por 'Produtivo'
    # para evitar perda de mensagens relevantes.
    if score < 0.6:
        return "Produtivo"

    # Garantia final de consistência do retorno.
    return label if label in LABELS else "Produtivo"

def generate_reply(category, original_text):
    """
    Gera uma resposta automática baseada na classificação do email.

    Lógica simples e baseada em regras fixas:
    - Emails classificados como 'Improdutivo' recebem uma resposta cordial e genérica.
    - Emails classificados como 'Produtivo' recebem uma resposta padrão indicando
      que a mensagem será analisada e respondida posteriormente.

    Args:
        category (str): Categoria do email ("Produtivo" ou "Improdutivo").
        original_text (str): Texto original do email (não utilizado diretamente aqui,
            mas pode ser útil para futuras melhorias, como personalização).

    Returns:
        str: Texto da resposta automática.
    """
    # Resposta padrão para emails improdutivos
    if category == "Improdutivo":
        return (
            "Obrigado pelo seu contato. "
            "Permanecemos à disposição para qualquer necessidade ou esclarecimento."
        )

    # Resposta padrão para emails produtivos
    return (
        "Agradecemos o seu contato. "
        "Sua mensagem foi recebida e será analisada. "
        "Responderemos assim que possível."
    )
