import re

def heavy_clean_nlp(text):
    # 1. Normalizar para minúsculas
    text = text.lower()
    
    # Substituir underscore por espaço para tratar "falha_técnica" antes da limpeza
    text = text.replace('_', ' ')
    
    # 2. Regex: Mantém apenas letras (incluindo acentuadas), espaços e o símbolo %
    # O padrão [^a-zà-ú% ] remove tudo que não for letra, espaço ou o caractere de porcentagem
    text = re.sub(r'[^a-zà-ú% ]', '', text)
    
    # Tokenização por espaço
    tokens = text.split()
    
    # 3. Lista de Custom Stopwords (conectores e palavras de baixo valor semântico)
    # Importante: "não", "erro" e "falha" NÃO entram nesta lista para serem preservados
    custom_stopwords = {
        'o', 'a', 'os', 'as', 'em', 'de', 'do', 'da', 'ou', 'está', 
        'com', 'para', 'que', 'um', 'uma', 'é'
    }
    
    # Filtragem: remove as stopwords, mas mantém os termos essenciais e métricas (%)
    filtered_tokens = [w for w in tokens if w not in custom_stopwords]
    
    # 4. Retornar lista de tokens únicos (set) e ordenados alfabeticamente (sorted)
    return sorted(list(set(filtered_tokens)))

# --- Teste da Função ---
frase_teste = "O sinal NÃO está em 100%!!! Erro de conexão ou falha_técnica?"
resultado = heavy_clean_nlp(frase_teste)

print("Output do Processamento:")
print(resultado)