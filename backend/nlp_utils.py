import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# --- Downloads necessários para uso do NLTK ---
# O NLTK (Natural Language Toolkit) é uma biblioteca popular para processamento de linguagem natural.
# Aqui, é baixado os recursos de stopwords (palavras irrelevantes) e o WordNet (para lematização -> redução de palavras flexionadas).
# Esses downloads são necessários apenas uma vez; em produção, é comum configurar cache/local storage.
nltk.download('stopwords')
nltk.download('wordnet')

# --- Stopwords ---
# Stopwords são palavras comuns que geralmente não agregam significado semântico relevante.
# (ex.: "de", "a", "o", "e") -> Removê-las ajuda a reduzir ruído no processamento de texto.
stop_words = set(stopwords.words('portuguese'))

# --- Lematizador ---
# O lematizador reduz palavras à sua forma canônica (ex.: "correria", "correu", "correndo" → "correr").
# Isso é útil para normalizar o texto e melhorar análises semânticas.
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    """
    Pré-processa o texto para análise de NLP (Processamento de Linguagem Natural).

    Etapas aplicadas:
    1. **Normalização para minúsculas**:
       - Facilita comparações e evita duplicidade entre palavras com maiúsculas/minúsculas.
    2. **Remoção de caracteres não alfabéticos**:
       - Uso de regex para manter apenas letras (incluindo acentos) e espaços.
       - Isso remove números, pontuação e símbolos que não são relevantes para análise semântica.
    3. **Tokenização simples**:
       - Divisão do texto em palavras usando "split()".
    4. **Remoção de stopwords**:
       - Remoção de palavras irrelevantes para reduzir ruído.
    5. **Lematização**:
       - Redução de cada palavra à sua forma base, melhorando consistência semântica.
    6. **Reconstrução do texto**:
       - Junção de palavras processadas em uma única string para uso posterior.

    Args:
        text (str): Texto bruto a ser pré-processado.

    Returns:
        str: Texto limpo e normalizado, pronto para análise.
    """
    # --- Tudo em minúsculas ---
    text = text.lower()
    # --- Regex para remover caracteres não alfabéticos ---
    text = re.sub(r'[^a-záàâãéêíóôõúç ]', '', text)
    # --- Tokenização ---
    words = text.split()
    # --- Remoção de stopwords + lematização ---
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    # --- Reconstrução do texto ---
    return ' '.join(words)
