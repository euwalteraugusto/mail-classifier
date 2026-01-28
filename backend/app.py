from flask import Flask, render_template, request
from nlp_utils import preprocess_text
from ai_service import classify_email, generate_reply
import pdfplumber
import os

# --- Diretório base do backend ---
# Uso de os.path para obter o caminho absoluto do arquivo atual (__file__).
# Isso garante que os diretórios de templates e static sejam resolvidos corretamente
# independentemente de onde o servidor for iniciado.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Configuração do Flask ---
# Definir explicitamente os diretórios de templates e arquivos estáticos.
# Separação importante para manter a arquitetura organizada:
# - frontend/templates → HTML
# - frontend/static → CSS, JS
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../frontend/templates"),
    static_folder=os.path.join(BASE_DIR, "../frontend/static")
)

@app.route('/', methods=['GET', 'POST'])
def index():
    # --- 1. Inicialização de variáveis ---
    # Definir aqui no topo garante que o 'render_template' sempre as encontre,
    # mesmo que o bloco POST não seja executado (evita UnboundLocalError).
    category = None
    reply = None
    content = ''
    source = None  # Inicializamos a nova variável aqui

    if request.method == 'POST':
        # --- 1. Prioridade: arquivo enviado ---
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

        # --- 2. Fallback: texto digitado manualmente ---
        if not content:
            content = request.form.get('email_text', '').strip()

        # --- 3. Processamento apenas se houver conteúdo válido ---
        if content:
            processed = preprocess_text(content)

            # A função agora retorna um dicionário: {'label': ..., 'source': ...}
            result = classify_email(processed)

            category = result.get('label')
            source = result.get('source') 

            reply = generate_reply(category, content)

    # --- 4. Renderização final ---
    # Como as variáveis foram inicializadas no topo, passar 'source=source' é seguro.
    return render_template(
        'index.html',
        category=category,
        reply=reply,
        content=content,
        source=source 
    )

if __name__ == '__main__':
    # Executa o servidor Flask em modo debug.
    # Modo debug:
    # - Atualiza automaticamente ao salvar alterações.
    # - Exibe erros detalhados no navegador.
    # Em produção, deve ser desativado por questões de segurança
    app.run(debug=False)
