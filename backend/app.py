from flask import Flask, render_template, request
from nlp_utils import preprocess_text
from ai_service import classify_email, generate_reply
import pdfplumber
import os

# Diretório base do backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuração do Flask
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../frontend/templates"),
    static_folder=os.path.join(BASE_DIR, "../frontend/static")
)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Inicialização de variáveis -> Garante que o 'render_template' sempre as encontre,
    mesmo que o bloco POST não seja executado (evita UnboundLocalError).
    """
    category = None
    reply = None
    content = ''
    source = None

    if request.method == 'POST':
        # Prioridade: arquivo enviado ---
        file = request.files.get('email_file')

        if file and file.filename:
            if file.filename.lower().endswith('.txt'):
                content = file.read().decode('utf-8', errors='ignore')

            elif file.filename.lower().endswith('.pdf'):
                try:
                    with pdfplumber.open(file) as pdf:
                        pages_text = [page.extract_text() for page in pdf.pages if page.extract_text()]
                        content = '\n'.join(pages_text)
                except Exception:
                    content = ''

        # Fallback: texto digitado manualmente
        if not content:
            content = request.form.get('email_text', '').strip()

        # Processamento apenas se houver conteúdo válido
        if content:
            # Limpeza de espaços/ quebras de linha excessivas
            content = content.strip()
            
            # A função agora retorna um dicionário: {'label': ..., 'source': ...}
            result = classify_email(content)

            category = result.get('label')
            source = result.get('source') 
            reply = generate_reply(category, content)

    # --- Renderização final ---
    # Como as variáveis foram inicializadas no topo, passar 'source=source' é seguro.
    return render_template(
        'index.html',
        category=category,
        reply=reply,
        content=content,
        source=source 
    )

if __name__ == '__main__':
    app.run(debug=False)
