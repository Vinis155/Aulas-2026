import nltk
import ssl

# Contornar problema com certificado SSL em alguns ambientes
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Baixar pacote necessário para tokenização (força download)
print("Baixando recursos NLTK necessários...")
nltk.download('punkt_tab')

# Importar tokenizador de palavras
from nltk.tokenize import word_tokenize

texto = "Machine Learning é uma das áreas mais importantes da Inteligência Artificial."

# Tokeniza o texto (divide em palavras)
tokens = word_tokenize(texto)

# Conta a quantidade de tokens
quantidade_tokens = len(tokens)

# Mostra os tokens encontrados
print(tokens)

# Mostra a quantidade de tokens
print(f"A quantidade de tokens na mensagem é: {quantidade_tokens}")
