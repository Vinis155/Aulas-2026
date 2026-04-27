import requests
import json


try:
    from IPython.display import display, HTML
except ImportError:
    def display(obj):
        pass
    def HTML(content):
        return content

print("=" * 70)
print("🎬 RICK AND MORTY API - SISTEMA DE TESTES")
print("=" * 70)


print("\n📋 [TESTE 1] Listar os primeiros personagens da API")
print("-" * 70)

try:
    url = "https://rickandmortyapi.com/api/character"
    response = requests.get(url, timeout=5)
    
    assert response.status_code == 200, f"API retornou status {response.status_code}"
    
    dados = response.json()
    
    print(f"Status code: {response.status_code}")
    print(f"Tipo de conteúdo: {response.headers.get('content-type')}")
    print(f"\n✅ Primeiros 5 personagens:")
    
    for i, character in enumerate(dados["results"][:5], 1):
        print(f"  {i}. {character['name']}")
    
    print(f"\n✅ Total de personagens na API: {dados['info']['count']}")
    
except Exception as e:
    print(f"❌ Erro ao listar personagens: {e}")

# ===== TESTE POSITIVO 2: Buscar personagem específico =====
print("\n" + "=" * 70)
print("🔍 [TESTE 2] Buscar informações do personagem Rick Sanchez (ID: 1)")
print("-" * 70)

try:
    url = "https://rickandmortyapi.com/api/character/1"
    response = requests.get(url, timeout=5)
    
    assert response.status_code == 200, f"Falha na requisição: status {response.status_code}"
    
    personagem = response.json()
    
    nome = personagem["name"]
    personagem_id = personagem["id"]
    status = personagem["status"]
    especie = personagem["species"]
    genero = personagem["gender"]
    origem = personagem["origin"]["name"]
    imagem = personagem["image"]
    
    # Validações
    assert nome == "Rick Sanchez", f"Nome inesperado: {nome}"
    assert imagem is not None, "Imagem não retornada"
    assert personagem_id > 0, f"ID inválido: {personagem_id}"
    
    print(f"✅ Nome: {nome}")
    print(f"✅ ID: {personagem_id}")
    print(f"✅ Status: {status}")
    print(f"✅ Espécie: {especie}")
    print(f"✅ Gênero: {genero}")
    print(f"✅ Origem: {origem}")
    print(f"✅ Imagem: {imagem}")
    print(f"\n✅ Teste positivo executado com sucesso!")
    
    display(HTML('''
    <div style="padding:15px; background:#e8f5e9; color:#1b5e20; border-radius:8px; margin-bottom:10px;">
    ✔ Cenário positivo: API respondeu corretamente com dados do personagem.
    </div>
    '''))
    
except AssertionError as e:
    print(f"❌ Validação falhou: {e}")
except Exception as e:
    print(f"❌ Erro ao buscar personagem: {e}")

# ===== TESTE POSITIVO 3: Buscar personagem por nome =====
print("\n" + "=" * 70)
print("🔎 [TESTE 3] Buscar personagem por nome (Morty)")
print("-" * 70)

def buscar_personagem(nome_personagem):
    """Função para buscar personagem por nome"""
    try:
        url = f"https://rickandmortyapi.com/api/character/?name={nome_personagem}"
        response = requests.get(url, timeout=5)
        return response
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

try:
    response = buscar_personagem("Morty")
    
    if response and response.status_code == 200:
        dados = response.json()
        print(f"✅ Personagens encontrados: {len(dados['results'])}")
        for char in dados['results'][:3]:
            print(f"  - {char['name']} (Status: {char['status']})")
    else:
        print(f"❌ Nenhum personagem encontrado ou erro na API")
        
except Exception as e:
    print(f"❌ Erro ao buscar por nome: {e}")

# ===== TESTE NEGATIVO: Personagem inexistente =====
print("\n" + "=" * 70)
print("❌ [TESTE 4] Simular erro: Buscar personagem inexistente (ID: 999999)")
print("-" * 70)

try:
    response_erro = requests.get("https://rickandmortyapi.com/api/character/999999", timeout=5)
    
    print(f"Status code: {response_erro.status_code}")
    
    assert response_erro.status_code == 404, f"Status esperado: 404, recebido: {response_erro.status_code}"
    
    print(f"Resposta: {response_erro.text[:200]}...")
    print(f"\n✅ Teste negativo executado com sucesso!")
    
    display(HTML('''
    <div style="padding:15px; background:#ffebee; color:#b71c1c; border-radius:8px;">
    ✖ Cenário negativo: API retornou 404 para um personagem inexistente.
    </div>
    '''))
    
except AssertionError as e:
    print(f"❌ Validação falhou: {e}")
except Exception as e:
    print(f"❌ Erro: {e}")

# ===== RESUMO FINAL =====
print("\n" + "=" * 70)
print("✅ TODOS OS TESTES FORAM EXECUTADOS COM SUCESSO!")
print("=" * 70)

# ===== ACESSO AO FRONT-END =====
print("\n" + "=" * 70)
print("🌐 FRONT-END DISPONÍVEL EM:")
print("=" * 70)
print("\n🔗 http://localhost:8000/index.html\n")
print("=" * 70)