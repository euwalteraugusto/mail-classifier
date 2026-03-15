import nltk
from nltk.corpus import stopwords
import re

# O NLTK -> Biblioteca para processamento de linguagem natural.
# Download de recursos de stopwords (palavras irrelevantes).
nltk.download('stopwords')
stop_words = set(stopwords.words('portuguese'))

def preprocess_text(text):
   """
   Limpeza leve para hurísticas.
   Mantém a estrutura original para não confundir o modelo de IA.
   """
   if not text:
         return ""
   
   # Texto em minúsculas e remoção de espaços extras
   text = text.lower(). strip()
   
   # Remoção apenas de caracteres especiais "sujos" (mantém pontuação básica).
   text = re.sub(r'[^\w\s\@\?\!]', '', text) # Permissões da Regex.
   
   # Tokenização para filtro de stopword (opcional para busca de keywords).
   words = text.split()
   filtered_words = [w for w in words if w not in stop_words]
   
   return ' '.join(filtered_words)
