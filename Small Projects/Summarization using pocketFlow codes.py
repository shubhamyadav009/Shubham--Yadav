# ---------------------------------------------
# PocketFlow Chatbot Assignment
# ---------------------------------------------

# Install required packages (run once)
# !pip install pocketflow
# !pip install -q -U google-genai
# !pip install python-dotenv

# ---------------------------------------------
# Imports
# ---------------------------------------------
import os
from dotenv import load_dotenv
from pocketflow import Node, Flow
from google import genai

# ---------------------------------------------
# Load API key from .env
# ---------------------------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file!")

# ---------------------------------------------
# Helper function to call LLM
# ---------------------------------------------
def call_llm(messages):
    """
    Calls the LLM (Gemini) with the conversation history.
    """
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=f"{messages}"
    )
    return response.text

# ---------------------------------------------
# Custom ChatNode class
# ---------------------------------------------
class ChatNode(Node):
    def prep(self, shared):
        """
        Prepare: Get user input and store in conversation history.
        """
        if "messages" not in shared:
            shared["messages"] = []
            print("Welcome! Type 'exit' to end the chat.")

        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            return None  # Exit conversation

        shared["messages"].append({"role": "user", "content": user_input})
        return shared["messages"]

    def exec(self, messages):
        """
        Execution: Call LLM to get assistant response.
        """
        if messages is None:
            return None
        return call_llm(messages)

    def post(self, shared, prep_res, exec_res):
        """
        Post: Print response, store it, and loop.
        """
        if prep_res is None or exec_res is None:
            print("\nGoodbye!")
            return None

        shared["messages"].append({"role": "assistant", "content": exec_res})
        print(f"\nAssistant: {exec_res}")
        return "continue"  # Loop back

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

# ---------------------------------------------
# Setup Chat Flow with Self-loop
# ---------------------------------------------
chat_node = ChatNode()
chat_node - "continue" >> chat_node  # Node loops back to itself

flow = Flow(start=chat_node)

# ---------------------------------------------
# Run the chat
# ---------------------------------------------
shared_data = {}
flow.run(shared_data)

# ---------------------------------------------
# Optional: Print full conversation history
# ---------------------------------------------
print("\n--- Full Conversation History ---")
for msg in shared_data["messages"]:
    print(f"{msg['role']}: {msg['content']}")
