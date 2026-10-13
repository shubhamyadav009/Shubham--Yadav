from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Load Embedding Model

model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Knowledge Base

documents = [
    "My name is Shubham.",
    "RAG stands for Retrieval-Augmented Generation.",
    "Most beautiful country in the world is India.",
    "Semantic search finds documents based on meaning instead of keywords.",
    "Embeddings are numerical representations of text.",
    "Vector databases store embeddings for similarity search.",
    "FAISS is used for fast vector similarity search.",
    "Cosine similarity measures how close two vectors are in direction."
    "Funny people make the world a better place.",
]

# Chunking
def chunk_text(text, chunk_size=8, overlap=2):
    """
    Splits text into overlapping chunks
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks

# Create chunks from documents
chunked_documents = []

for doc in documents:
    chunks = chunk_text(doc)
    chunked_documents.extend(chunks)

# 3. Create Embeddings

doc_embeddings = model.encode(documents, convert_to_numpy=True)

# 4. Build FAISS Index

dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(doc_embeddings)

# 5. Semantic Search

def semantic_search(query, top_k=3):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    return [documents[i] for i in indices[0]]

# 6. RAG (Simple Response)

def rag_answer(query):
    retrieved_docs = semantic_search(query)
    return "\n".join(retrieved_docs)

# 7. Run Example

if __name__ == "__main__":
    query = "Explain semantic search and how it is used in RAG and which is most beautiful country "
    print("Retrieved Context:")
    print(rag_answer(query))
