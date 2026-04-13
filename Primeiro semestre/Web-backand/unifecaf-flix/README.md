# 🎬 UniFECAF Flix API

Uma API moderna e escalável para gerenciamento de filmes, desenvolvida com Node.js, Express, Prisma e PostgreSQL.

## 📋 Pré-requisitos

- Node.js (v14 ou superior)
- PostgreSQL (instalado e rodando)
- npm ou yarn

## 🚀 Instalação Rápida

### 1. Clonar o repositório e instalar dependências
```bash
cd unifecaf-flix
npm install
```

### 2. Configurar o banco de dados

#### Passo 2.1: Criar o banco de dados PostgreSQL
```sql
CREATE DATABASE unifecaf_flix;
```

#### Passo 2.2: Atualizar o arquivo `.env`
Edite o arquivo `.env` na raiz do projeto e configure a string de conexão:

```env
DATABASE_URL="postgresql://seu_usuario:sua_senha@localhost:5432/unifecaf_flix?schema=public"
```

Substitua:
- `seu_usuario`: Seu usuário PostgreSQL (padrão: `postgres`)
- `sua_senha`: Sua senha PostgreSQL

#### Passo 2.3: Executar as migrations
```bash
npm run migrate
```

Este comando criará a tabela de filmes automaticamente.

#### Passo 2.4: Gerar o cliente Prisma
```bash
npm run generate
```

### 3. Iniciar o servidor

**Modo Desenvolvimento (com auto-reload):**
```bash
npm run dev
```

**Modo Produção:**
```bash
npm start
```

O servidor estará disponível em: `http://localhost:3000`

## 📡 Endpoints da API

### 1. Health Check
```
GET /health
```
Verifica se a API está online.

**Resposta (200):**
```json
{
  "statusCode": 200,
  "message": "API está online e funcionando",
  "timestamp": "2026-04-10T10:30:00.000Z"
}
```

---

### 2. Listar Todos os Filmes
```
GET /v1/controle-filmes/filme
```
Retorna todos os filmes cadastrados no banco.

**Resposta (200):**
```json
{
  "statusCode": 200,
  "message": "Filmes recuperados com sucesso",
  "data": [
    {
      "id": 1,
      "nome": "Inception",
      "sinopse": "Um filme sobre sonhos e realidade",
      "duracao": 148,
      "genero": "Ficção Científica",
      "capaUrl": "https://exemplo.com/capa.jpg",
      "criadoEm": "2026-04-10T10:00:00.000Z",
      "atualizadoEm": "2026-04-10T10:00:00.000Z"
    }
  ]
}
```

---

### 3. Buscar Filme por ID
```
GET /v1/controle-filmes/filme/:id
```

**Parâmetros:**
- `id` (URL): ID do filme a buscar

**Exemplo:**
```
GET /v1/controle-filmes/filme/1
```

**Respostas:**

✅ **Sucesso (200):**
```json
{
  "statusCode": 200,
  "message": "Filme encontrado com sucesso",
  "data": {
    "id": 1,
    "nome": "Inception",
    "sinopse": "Um filme sobre sonhos e realidade",
    "duracao": 148,
    "genero": "Ficção Científica",
    "capaUrl": "https://exemplo.com/capa.jpg",
    "criadoEm": "2026-04-10T10:00:00.000Z",
    "atualizadoEm": "2026-04-10T10:00:00.000Z"
  }
}
```

❌ **Não Encontrado (404):**
```json
{
  "statusCode": 404,
  "message": "Filme com ID 999 não encontrado"
}
```

❌ **ID Inválido (400):**
```json
{
  "statusCode": 400,
  "message": "ID deve ser um número inteiro válido"
}
```

---

### 4. Filtrar Filmes por Nome ou Sinopse
```
GET /v1/controle-filmes/filtro/filme?nome=xxx
```

**Parâmetros (Query String):**
- `nome` (obrigatório): Texto para buscar (case-insensitive)

**Exemplos:**
```
GET /v1/controle-filmes/filtro/filme?nome=Inception
GET /v1/controle-filmes/filtro/filme?nome=sonhos
GET /v1/controle-filmes/filtro/filme?nome=ficção
```

**Resposta (200):**
```json
{
  "statusCode": 200,
  "message": "Filmes encontrados com o termo \"Inception\"",
  "data": [
    {
      "id": 1,
      "nome": "Inception",
      "sinopse": "Um filme sobre sonhos e realidade",
      "duracao": 148,
      "genero": "Ficção Científica",
      "capaUrl": "https://exemplo.com/capa.jpg",
      "criadoEm": "2026-04-10T10:00:00.000Z",
      "atualizadoEm": "2026-04-10T10:00:00.000Z"
    }
  ],
  "total": 1
}
```

**Erro - Parâmetro Vazio (400):**
```json
{
  "statusCode": 400,
  "message": "Parâmetro 'nome' é obrigatório e não pode ser vazio"
}
```

---

## 🗂️ Estrutura do Projeto

```
unifecaf-flix/
├── src/
│   ├── controllers/
│   │   └── filmeController.js    # Lógica de endpoints
│   ├── routes/
│   │   └── filmeRoutes.js        # Definição de rotas
│   ├── services/
│   │   └── filmeService.js       # Lógica de negócio reutilizável
│   └── server.js                 # Arquivo principal da API
├── prisma/
│   └── schema.prisma             # Modelagem do banco de dados
├── .env                          # Variáveis de ambiente
├── .gitignore                    # Arquivos ignorados no Git
├── package.json                  # Dependências do projeto
└── README.md                     # Este arquivo
```

---

## 📦 Dependências

### Runtime
- **express**: Framework web minimalista
- **@prisma/client**: Client ORM para interagir com o banco
- **dotenv**: Gerenciador de variáveis de ambiente

### Development
- **nodemon**: Restart automático do servidor durante desenvolvimento
- **prisma**: CLI para migrations e gerenciamento de schema

---

## ✅ Boas Práticas Implementadas

✔️ **Try/Catch em todos os endpoints** - Tratamento robusto de erros com resposta JSON padronizada
✔️ **Modularização completa** - Separação de controllers, routes e services
✔️ **Validação de entrada** - Verificação de tipos e formatos
✔️ **Responses padronizadas** - Todas as respostas seguem um padrão consistente
✔️ **HTTP Status Codes corretos** - Uso apropriado de 200, 400, 404, 500
✔️ **Segurança SQL** - Uso de ORM para prevenir SQL Injection
✔️ **Case-insensitive search** - Busca flexível com `mode: 'insensitive'` do Prisma

---

## 🐛 Troubleshooting

### Erro: "Cannot find module '@prisma/client'"
```bash
npm install
npm run generate
```

### Erro: "connect ECONNREFUSED 127.0.0.1:5432"
Certifique-se de que o PostgreSQL está rodando:
- Linux/Mac: `sudo service postgresql start`
- Windows: Verifique os Serviços do Windows

### Erro: "Database does not exist"
```sql
CREATE DATABASE unifecaf_flix;
npm run migrate
```

---

## 📝 Exemplo de Uso com cURL

```bash
# Health check
curl http://localhost:3000/health

# Listar todos os filmes
curl http://localhost:3000/v1/controle-filmes/filme

# Buscar filme por ID
curl http://localhost:3000/v1/controle-filmes/filme/1

# Filtrar filmes
curl "http://localhost:3000/v1/controle-filmes/filtro/filme?nome=Inception"
```

---

## 🎓 Próximos Passos

Para melhorar ainda mais a API, considere:
- Adicionar endpoints POST, PUT, DELETE para criar/atualizar/deletar filmes
- Implementar autenticação e autorização
- Adicionar testes automatizados
- Configurar CORS para frontend
- Implementar paginação
- Adicionar logs mais detalhados

---

**Desenvolvido para UniFECAF - 2026**
