# API de Inteligência Artificial Acadêmica

API desenvolvida como trabalho final da disciplina **Construção de APIs para Inteligência Artificial** (UFG).

Disponibiliza dois serviços de IA para suporte acadêmico, utilizando **FastAPI** e **Hermes Agent** (NousResearch):

| Endpoint | Descrição |
|---|---|
| `POST /v1/ask` | Tira dúvidas sobre o conteúdo das aulas (consulta PDFs) |
| `POST /v1/tasks` | Consulta tarefas, documentos e prazos de entrega |

---

## Estrutura do projeto

```
.
├── app/
│   ├── agents/
│   │   ├── content_agent.py   # Agente de conteúdo (PDFs de aula)
│   │   └── tasks_agent.py     # Agente de tarefas e prazos
│   ├── api/v1/
│   │   ├── content.py         # Endpoint POST /v1/ask
│   │   └── tasks.py           # Endpoint POST /v1/tasks
│   ├── core/
│   │   ├── config.py          # Configurações e variáveis de ambiente
│   │   ├── logger.py          # Logger centralizado
│   │   └── security.py        # Autenticação via X-API-Key
│   └── main.py                # Aplicação FastAPI
├── data/
│   ├── aulas/                 # Coloque aqui os PDFs de conteúdo das aulas
│   └── tarefas/               # Coloque aqui o DOCX/PDF de tarefas
├── tests/
│   └── test_endpoints.py      # Testes automatizados
├── logs/                      # Gerado automaticamente
├── .env.example
├── requirements.txt
└── README.md
```

---

## Pré-requisitos

- Python 3.11+
- Conta no [OpenRouter](https://openrouter.ai) (para acessar os modelos via Hermes)

---

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` e preencha:

```env
OPENROUTER_API_KEY=sua_chave_openrouter
API_SECRET_KEY=qualquer_string_segura
AI_MODEL=deepseek/deepseek-v4-flash
LOG_LEVEL=INFO
```

### 5. Adicione os arquivos de dados

- Coloque os **PDFs das aulas** em `data/aulas/`
- Coloque o **documento de tarefas** (`.docx` ou `.pdf`) em `data/tarefas/`

### 6. Execute a API

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: http://localhost:8000

Documentação interativa (Swagger): http://localhost:8000/docs

---

## Como usar

### Autenticação

Todas as rotas exigem o header `X-API-Key` com o valor definido em `API_SECRET_KEY`.

### Exemplos com curl

**Tirar dúvida sobre conteúdo de aula:**
```bash
curl -X POST http://localhost:8000/v1/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sua_chave" \
  -d '{"question": "O que é autenticação JWT?"}'
```

**Consultar tarefas e prazos:**
```bash
curl -X POST http://localhost:8000/v1/tasks \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sua_chave" \
  -d '{"question": "Quais tarefas vencem essa semana?"}'
```

---

## Testes

```bash
pip install pytest httpx
pytest tests/ -v
```

---

## Requisitos técnicos implementados

- **Validação de dados** — Pydantic v2 com tamanho mínimo/máximo de campos
- **Tratamento de erros** — HTTP 401, 404, 422, 500 com mensagens descritivas
- **Logs** — Arquivo `logs/app.log` + saída no terminal, com nível configurável
- **Segurança** — Autenticação via header `X-API-Key`
- **Versionamento** — Prefixo `/v1/` em todas as rotas de IA
