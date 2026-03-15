import os
from groq import Groq
import json
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Busca a chave de forma segura
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def classify_email(raw_text):
    """
    Classificação de e-mail utilizando Llama 3 via Groq.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um classificador de e-mails corporativos especializado em triagem de tarefas. "
                        "Sua saída deve ser EXCLUSIVAMENTE um JSON válido. "
                        "Classifique o e-mail em: PRODUTIVO ou IMPRODUTIVO.\n\n"
                        "CRITÉRIOS:\n"
                        "- PRODUTIVO: Solicitações de ação, prazos, dúvidas sobre projetos, cobranças, agendamentos, "
                        "documentos anexos importantes ou perguntas sobre status.\n"
                        "- IMPRODUTIVO: Apenas saudações, agradecimentos, mensagens automáticas de 'out of office', "
                        "confirmações simples (ex: 'ok', 'ciente') ou conversas casuais.\n\n"
                        "Exemplo de saída: {\"label\": \"Produtivo\", \"source\": \"Llama 3 (Justificativa curta)\"}"
                    )
                },
                {
                    "role": "user",
                    "content": f"Classifique este e-mail: '{raw_text}'"
                }
            ],
            model="llama-3.1-8b-instant", # Modelo rápido e gratuito
            response_format={"type": "json_object"} # Resposta em JSON
        )

        # Parse da resposta
        res_content = json.loads(chat_completion.choices[0].message.content)
        label_returned = res_content.get("label", "Improdutivo").capitalize() # Garante que seja "Produtivo" ou "Improdutivo"
        
        # Padronizando o retorno para o seu app.py
        return {
            "label": label_returned,
            "source": res_content.get("source", "Llama 3 Analysis")
        }

    except Exception as e:
        # Fallback caso a API falhe ou a chave não esteja configurada
        return {"label": "Improdutivo", "source": f"Erro na API: {str(e)}"}

def generate_reply(category, original_text):
    if category == "Produtivo":
        return "Sua solicitação foi identificada. Estamos processando as informações."
    return "Mensagem recebida. Nenhuma ação imediata necessária."