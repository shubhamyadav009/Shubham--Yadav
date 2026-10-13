# -------------------------------
# Expert RAG Chatbot using PocketFlow
# -------------------------------

from pocketflow import Node, Flow

# -------------------------------
# Mock Document Store
# -------------------------------
DOCUMENTS = {
    "python": "Python is a high-level, interpreted programming language.",
    "pocketflow": "PocketFlow is a Python library for building workflow flows and nodes.",
    "rag": "RAG stands for Retrieval-Augmented Generation. It combines retrieval with LLM generation.",
    "hi": "Hi there! I'm your assistant.",
    "hello": "Hello! How can I help you today?",
    "assignment": "You can ask me about coding, PocketFlow, FSMs, Chatbots, and more."
}

# -------------------------------
# Mock LLM Call
# -------------------------------
def generate_answer(query, context):
    """
    Simulate an LLM generating an answer using retrieved context.
    """
    context_text = "\n".join(context)
    return f"Based on your query '{query}' and context:\n{context_text}\nMy answer: [This is an AI-generated expert response]"

# -------------------------------
# Retrieval Node
# -------------------------------
class ExpertRAGNode(Node):
    def prep(self, shared):
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit", "end"]:
            return None
        return query

    def exec(self, query):
        if query is None:
            return None

        # Retrieve relevant docs
        query_words = query.lower().split()
        context = []
        for key, doc in DOCUMENTS.items():
            if key in query_words:
                context.append(doc)

        if not context:
            context = ["Sorry, no relevant documents found."]

        # Generate an expert answer
        answer = generate_answer(query, context)
        return {"query": query, "context": context, "answer": answer}

    def post(self, shared, prep_res, exec_res):
        if prep_res is None or exec_res is None:
            print("\nGoodbye! Conversation ended.")
            return None

        # Print retrieved context and AI answer
        print(f"\nAssistant:\n{exec_res['answer']}")

        # Save conversation in shared store
        if "messages" not in shared:
            shared["messages"] = []
        shared["messages"].append({"role": "user", "content": prep_res})
        shared["messages"].append({"role": "assistant", "content": exec_res['answer']})

        return "continue"

# -------------------------------
# Flow setup
# -------------------------------
shared_store = {}
chat_node = ExpertRAGNode()
chat_node - "continue" >> chat_node  # self-loop

flow = Flow(start=chat_node)

# -------------------------------
# Start Chatbot
# -------------------------------
print("Welcome to Expert RAG Chatbot! Type 'exit', 'quit', or 'end' to stop.")
flow.run(shared_store)

# -------------------------------
# Print conversation history
# -------------------------------
print("\nConversation History:")
for msg in shared_store.get("messages", []):
    print(f"{msg['role']}: {msg['content']}")
