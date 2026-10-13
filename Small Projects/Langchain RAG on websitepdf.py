# ------------------------------
# 1. Load Website Data
# ------------------------------
from langchain_community.document_loaders import WebBaseLoader

website_loader = WebBaseLoader(
    "https://docs.langchain.com/oss/python/langchain/overview"
)
website_docs = website_loader.load()
print(f"Loaded {len(website_docs)} document(s) from website.")

# ------------------------------
# 2. Load PDF Data
# ------------------------------
from langchain_community.document_loaders import PyPDFLoader

pdf_loader = PyPDFLoader(
    r"C:/Users/yadav/OneDrive/Desktop/Hey09/GenAi-2/PYTHON INTERVIEW.pdf"
)
pdf_docs = pdf_loader.load()
print(f"Loaded {len(pdf_docs)} document(s) from PDF.")

# ------------------------------
# 3. Combine Documents
# ------------------------------
documents = website_docs + pdf_docs
print(f"Total documents combined: {len(documents)}")

# ------------------------------
# 4. Split Text into Chunks
# ------------------------------
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
splits = text_splitter.split_documents(documents)
print(f"Total chunks created: {len(splits)}")

# ------------------------------
# 5. Prepare Texts Safely and Create Embeddings
# ------------------------------
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Extract and sanitize plain text from Document objects
texts = []
for i, doc in enumerate(splits):
    content = doc.page_content
    if isinstance(content, str) and content.strip():  # must be a non-empty string
        texts.append(content.strip())
    else:
        print(f"Skipping invalid chunk at index {i}")

print(f"Total valid chunks for embedding: {len(texts)}")

# Create embeddings
embeddings = HuggingFaceEmbeddings(model="all-MiniLM-L6-v2")
vectorstore = FAISS.from_texts(texts, embeddings)
print("Vectorstore created successfully.")

# ------------------------------
# 6. Create Retriever
# ------------------------------
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ------------------------------
# 7. Set up Gemini LLM with RetrievalQA
# ------------------------------
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.retrieval_qa import RetrievalQA

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    api_key=api_key
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# ------------------------------
# 8. Query Loop
# ------------------------------
print("\nLangChain RAG is ready! Type 'exit' to quit.\n")

while True:
    query = input("Ask a question: ")
    if query.lower() == "exit":
        break

    result = qa_chain.invoke({"query": query})

    print("\nAnswer:\n", result["result"])
    print("\nSources:")
    for doc in result["source_documents"]:
        print("-", doc.metadata.get("source", "Unknown"))
