import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

VARIAVEIS_AMBIENTE = (
    "GOOGLE_API_KEY",
    "DATABASE_URL",
    "PG_VECTOR_COLLECTION_NAME",
    "GOOGLE_CHAT_MODEL",
    "GOOGLE_EMBEDDING_MODEL"
)

for k in VARIAVEIS_AMBIENTE:
    if not os.getenv(k):
        raise RuntimeError(f"A variável de ambiente {k} não foi definida.")

database_url = os.getenv("DATABASE_URL")
pg_vector_collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
embedding_model_name = os.getenv("GOOGLE_EMBEDDING_MODEL")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model_name)

pg_vector = PGVector(
    collection_name=pg_vector_collection_name,
    connection=database_url,
    embeddings=embeddings,
    use_jsonb=True
)

def search_engine(query: str) -> list[str]:
    try:
        results = pg_vector.similarity_search(query, k=10)
        return [result.page_content for result in results]
    except Exception as e:
        print(f"Erro durante o processo de busca: {e}")
        return []

def search_prompt(question: str) -> str:
    if not question:
        return ""
        
    contexto = "\n\n".join(search_engine(question))
    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)
    return prompt
