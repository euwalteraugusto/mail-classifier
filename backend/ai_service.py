from transformers import pipeline

# Adicionamos 'Irrelevante' para capturar mensagens aleatórias/spam
LABELS = ["Produtivo", "Improdutivo", "Irrelevante"]

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

def classify_email(text):
    normalized_text = text.strip().lower()

    # 1. Filtro de Relevância (Heurística Anti-Aleatoriedade)
    # Se não houver termos mínimos de contexto corporativo ou sinais de pontuação úteis, 
    # classificamos como irrelevante para poupar processamento.
    corporate_context = [
        "segue", "anexo", "encaminho", "solicito", "reunião", "projeto", 
        "prazo", "contrato", "pagamento", "relatório", "contato", "ajuda",
        "dúvida", "informação", "prezado", "atenciosamente"
    ]
    
    # Se o texto for curto e não tiver contexto corporativo nem pergunta
    if len(normalized_text) < 50 and not any(word in normalized_text for word in corporate_context) and "?" not in normalized_text:
        return {"label": "Improdutivo", "source": "Filtro de Contexto (Mensagem Aleatória)"}

    # 2. Heurísticas de Curto Alcance (Custo Zero)
    if len(normalized_text) < 20:
        return {"label": "Improdutivo", "source": "Heurística (Tamanho Insuficiente)"}

    cordial_expressions = ["obrigado", "obrigada", "ok", "ciente", "entendido", "bom dia", "boa tarde", "boa noite"]
    if any(normalized_text == expr or normalized_text.startswith(expr + " ") for expr in cordial_expressions):
        return {"label": "Improdutivo", "source": "Heurística (Cordialidade)"}

    # 3. Heurística de Intenção Ativa
    response_intent_indicators = [
        "algum retorno", "aguardamos retorno", "aguardo retorno", "poderia informar",
        "poderia verificar", "status", "atualização", "posicionamento", "referente a"
    ]
    if "?" in normalized_text or any(indicator in normalized_text for indicator in response_intent_indicators):
        return {"label": "Produtivo", "source": "Heurística (Intenção Direta)"}

    # 4. Classificação Zero-Shot (O "Cérebro" do Sistema)
    result = classifier(
        text,
        candidate_labels=LABELS,
        hypothesis_template="Este texto é um email corporativo {}."
    )

    label = result["labels"][0]
    score = result["scores"][0]
    score_pct = round(score * 100, 1)

    # Lógica de Refino de Assertividade:
    # Se a maior probabilidade for 'Irrelevante', ou se a confiança for baixa (< 55%)
    if label == "Irrelevante" or score < 0.55:
        return {"label": "Improdutivo", "source": f"Modelo (Baixa Relevância: {score_pct}%)"}
    
    return {
        "label": label if label in ["Produtivo", "Improdutivo"] else "Improdutivo", 
        "source": f"Modelo Zero-Shot ({score_pct}% de confiança)"
    }

def generate_reply(category, original_text):
    """Gera respostas mais condizentes com o novo filtro."""
    if category == "Improdutivo":
        return "Mensagem recebida. Não identificamos necessidade de ação imediata. Permanecemos à disposição."
    
    return (
        "Sua mensagem foi classificada como prioritária. "
        "Iniciamos a análise e retornaremos com um posicionamento em breve."
    )