"""
RAG grounding for the grid agent.

Embeds a small curated set of grid market documents into pgvector, and exposes
a retrieval tool the agent uses to explain WHY grid conditions occur (what LMP
is, why prices differ by location, why fuel mix shifts) rather than only
reporting the numbers.

Run once to load the docs:   python grid_rag.py --ingest
Then the agent imports `explain_grid_concept`.
"""

import os
import glob
import hashlib

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()

# Set this to your local Postgres. Example:
# postgresql+psycopg://user:password@localhost:5432/griddb
CONNECTION = os.getenv("POSTGRES_URL", "postgresql+psycopg://localhost:5432/postgres").replace(
    "postgresql://", "postgresql+psycopg://", 1
)
COLLECTION = "grid_docs"

_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


_store_singleton: PGVector | None = None


def _store(pre_delete_collection: bool = False) -> PGVector:
    global _store_singleton
    if pre_delete_collection or _store_singleton is None:
        _store_singleton = PGVector(
            embeddings=_embeddings,
            collection_name=COLLECTION,
            connection=CONNECTION,
            use_jsonb=True,
            pre_delete_collection=pre_delete_collection,
        )
    return _store_singleton


def _chunk_id(source: str, index: int) -> str:
    # Stable per (source, position) so re-running ingest upserts instead of duplicating,
    # even when two chunks share identical text (e.g. repeated PDF headers/footers).
    return hashlib.sha256(f"{source}:{index}".encode()).hexdigest()


def ingest(docs_dir="grid_docs", reset: bool = False):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = []
    ids = []

    # markdown docs (as before)
    for path in sorted(glob.glob(os.path.join(docs_dir, "*.md"))):
        text = open(path).read()
        source = os.path.basename(path)
        for i, chunk in enumerate(splitter.split_text(text)):
            chunks.append(Document(page_content=chunk, metadata={"source": source}))
            ids.append(_chunk_id(source, i))

    # PDF docs (new)
    for path in sorted(glob.glob(os.path.join(docs_dir, "*.pdf"))):
        source = os.path.basename(path)
        pages = PyPDFLoader(path).load()          # one Document per page
        full_text = "\n".join(p.page_content for p in pages)
        for i, chunk in enumerate(splitter.split_text(full_text)):
            chunks.append(Document(page_content=chunk, metadata={"source": source}))
            ids.append(_chunk_id(source, i))

    _store(pre_delete_collection=reset).add_documents(chunks, ids=ids)
    print(f"Ingested {len(chunks)} chunks into '{COLLECTION}'.")


def retrieve(question: str, k: int = 3) -> dict:
    hits = _store().similarity_search(question, k=k)

    passages = []
    for h in hits:
        passages.append({
            "source": h.metadata.get("source", "?"),
            "text": h.page_content,
        })

    return {"question": question, "passages": passages}


if __name__ == "__main__":
    import sys
    if "--ingest" in sys.argv:
        ingest(reset="--reset" in sys.argv)
    else:
        # quick retrieval smoke test
        import json
        print(json.dumps(retrieve("why do electricity prices differ by location?"), indent=2))