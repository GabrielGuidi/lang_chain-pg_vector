import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

def ingest_pdf():
    load_dotenv()
    
    VARIAVEIS_AMBIENTE = (
        "GOOGLE_API_KEY", 
        "DATABASE_URL", 
        "PG_VECTOR_COLLECTION_NAME", 
        "PDF_NAME",
        "GOOGLE_EMBEDDING_MODEL"
    )
    
    for k in VARIAVEIS_AMBIENTE:
        if not os.getenv(k):
            raise RuntimeError(f"A variável de ambiente {k} não foi definida.")

    pdf_name = os.getenv("PDF_NAME")
    embedding_model = os.getenv("GOOGLE_EMBEDDING_MODEL")
    database_url = os.getenv("DATABASE_URL")
    pg_vector_collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")

    current_dir = Path(__file__).parent
    pdf_path = current_dir.parent / pdf_name

    if not pdf_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")

    print(f"Carregando documento: {pdf_path}.")
    docs = PyPDFLoader(str(pdf_path)).load()

    print("Dividindo o PDF em pedaços menores.")
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, 
        add_start_index=False
    ).split_documents(docs)

    if not splits:
        print("Nenhum texto extraído do PDF.")
        return

    print("Enriquecendo pedaços.")
    enriched = []
    for d in splits:
        clean_metadata = {k: v for k, v in d.metadata.items() if v not in ("", None)}
        enriched.append(Document(page_content=d.page_content, metadata=clean_metadata))

    ids = [f"doc-{i}" for i in range(len(enriched))]

    print(f"Total de chunks preparados para ingestão: {len(enriched)}")
    
    print("Conectando ao modelo de embeddings.")
    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)

    print("Iniciando ingestão no PostgreSQL.")
    store = PGVector(
        embeddings=embeddings,
        collection_name=pg_vector_collection_name,
        connection=database_url,
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)

    print("Ingestão concluída com sucesso.")

if __name__ == "__main__":
    ingest_pdf()