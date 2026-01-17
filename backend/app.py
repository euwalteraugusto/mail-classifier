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
    """
    Rota principal da aplicação.

    Fluxo de execução:
    1. **Receber entrada do usuário**:
       - Se um arquivo for enviado (prioridade), extrai o conteúdo.
       - Caso contrário, usa o texto digitado manualmente.
    2. **Pré-processamento**:
       - Normaliza o texto usando "preprocess_text" (remoção de ruído, stopwords, etc.).
    3. **Classificação**:
       - Usa "classify_email" para determinar se o email é "Produtivo" ou "Improdutivo".
    4. **Resposta automática**:
       - Gera uma resposta padrão com "generate_reply", baseada na categoria.
    5. **Renderização**:
       - Retorna o template "index.html" com os resultados.

    Returns:
        HTML: Página renderizada com categoria, resposta e conteúdo original.
    """

    # Inicializa variáveis para evitar erros caso não haja POST.
    category = None
    reply = None
    content = ''

    if request.method == 'POST':

        # --- 1. Prioridade: arquivo enviado ---
        # Se o usuário anexa um arquivo, tenta processá-lo primeiro.
        file = request.files.get('email_file')

        if file and file.filename:

            # --- Caso TXT ---
            # Leitura simples do conteúdo como string UTF-8.
            if file.filename.lower().endswith('.txt'):
                content = file.read().decode('utf-8', errors='ignore')

            # --- Caso PDF ---
            # Usa pdfplumber para extrair texto de cada página.
            # pdfplumber -> extração precisa de texto,
            # preservando estrutura básica sem precisar de OCR (Reconhecimento Óptico de Caracteres) IMAGEM -> TEXTO.
            elif file.filename.lower().endswith('.pdf'):
                try:
                    with pdfplumber.open(file) as pdf:
                        pages_text = []

                        # Processa todas as páginas do PDF.
                        for page in pdf.pages:
                            text = page.extract_text()
                            if text:
                                pages_text.append(text)

                        # Concatena o texto das páginas em uma única string.
                        content = '\n'.join(pages_text)

                # Em caso de erro na leitura do PDF, evita quebra de fluxo.
                except Exception:
                    content = ''

        # --- 2. Fallback: texto digitado manualmente ---
        # Se não houver arquivo válido, usamos o texto fornecido no formulário.
        if not content:
            content = request.form.get('email_text', '').strip()

        # --- 3. Processamento apenas se houver conteúdo válido ---
        if content:

            # Pré-processamento para normalizar o texto.
            processed = preprocess_text(content)

            # Classificação do email (Produtivo/Improdutivo).
            category = classify_email(processed)

            # Geração de resposta automática baseada na categoria.
            reply = generate_reply(category, content)

    # --- Renderização final ---
    # Passa os resultados para o template HTML.
    return render_template(
        'index.html',
        category=category,
        reply=reply,
        content=content
    )

if __name__ == '__main__':
    # Executa o servidor Flask em modo debug.
    # Modo debug:
    # - Atualiza automaticamente ao salvar alterações.
    # - Exibe erros detalhados no navegador.
    # Em produção, deve ser desativado por questões de segurança
    app.run(debug=False)
