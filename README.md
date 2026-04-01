# Desafio MBA Engenharia de Software com IA - Full Cycle

## Requisitos

- API Key do Google Gemini
- Python 3.10+
- Docker
- Docker Compose

## Configuração do ambiente

Siga o passo a passo abaixo na raiz do projeto.

1. Criar e ativar ambiente virtual (`venv`):

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:

- Duplique o arquivo `.env.example` e renomeie para `.env`
- Abra o arquivo `.env` e substitua os valores pelas suas chaves de API reais obtidas conforme instruções abaixo

4. Subir a infraestrutura (PostgreSQL + pgvector):

```bash
docker compose up -d
```

5. Executar ingestão do PDF:

```bash
python src/ingest.py
```

6. Rodar o chat:

```bash
python src/chat.py
```

- Digite sua pergunta e pressione Enter.
- Para encerrar, digite `sair`.

## Estrutura e limitações

- O assistente responde apenas com base no conteúdo extraído do PDF.
- Se a resposta não estiver no contexto, retorna: "Não tenho informações necessárias para responder sua pergunta."
- Não há memória de conversa entre perguntas.
- `ingest.py`: leitura do PDF, chunking e ingestão vetorial.
- `search.py`: busca semântica e template do prompt.
- `chat.py`: CLI de interação com o usuário.
- `docker-compose.yml`: serviços PostgreSQL e extensão pgvector.

## Como criar a API Key do Google Gemini

1. Acesse o Google AI Studio:

[https://ai.google.dev/gemini-api/docs/api-key?hl=pt-BR](https://ai.google.dev/gemini-api/docs/api-key?hl=pt-BR)

2. Faça login com sua conta Google.
3. Vá para a seção de API Keys.
4. Crie uma nova chave e copie o valor.

Documentação oficial:
[Como usar chaves da API Gemini](https://ai.google.dev/gemini-api/docs/api-key?hl=pt-BR)

Não compartilhe sua chave publicamente.
