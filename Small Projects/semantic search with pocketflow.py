from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# PocketFlow-style minimal framework

class Node:
    def run(self, data: dict) -> dict:
        raise NotImplementedError("Each node must implement run()")


class Flow:
    def __init__(self, nodes):
        self.nodes = nodes

    def run(self, data: dict) -> dict:
        for node in self.nodes:
            data = node.run(data)
        return data

# Load Embedding Model

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Knowledge Base

documents = [
    "RAG stands for Retrieval-Augmented Generation.",
    "Semantic search finds documents based on meaning instead of keywords.",
    "Embeddings are numerical representations of text.",
    "Vector databases store embeddings for similarity search.",
    "FAISS is used for fast vector similarity search.",
    "Cosine similarity measures how close two vectors are in direction."
]

# Create Document Embeddings

doc_embeddings = embedding_model.encode(documents, convert_to_numpy=True)

# Build FAISS Index

dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(doc_embeddings)

# Pipeline Nodes

class QueryEmbeddingNode(Node):
    def run(self, data):
        query = data["query"]
        data["query_embedding"] = embedding_model.encode(
            [query], convert_to_numpy=True
        )
        return data


class SemanticSearchNode(Node):
    def run(self, data):
        query_embedding = data["query_embedding"]
        distances, indices = index.search(query_embedding, 3)
        data["retrieved_docs"] = [documents[i] for i in indices[0]]
        return data


class RAGNode(Node):
    def run(self, data):
        context = "\n".join(data["retrieved_docs"])
        data["answer"] = f"""
RAG Retrieved Context
--------------------
{context}

(Note: This is retrieval-only RAG; no LLM generation.)
"""
        return data

# Build Flow (CORRECTED)

rag_flow = Flow([
    QueryEmbeddingNode(),
    SemanticSearchNode(),
    RAGNode()
])

# Run Flow

if __name__ == "__main__":
    result = rag_flow.run({
        "query": "Explain semantic search and how it is used in RAG"
    })

    print(result["answer"])
