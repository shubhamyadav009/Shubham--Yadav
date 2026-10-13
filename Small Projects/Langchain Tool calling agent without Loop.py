from langchain.tools import tool

# Define a simple tool
@tool
def search(query: str) -> str:
    """Return a predefined answer for the query"""
    data = {
        "capital of france": "Paris",
        "fashionmnist classes": "10 classes",
        "autoencoder example": "Autoencoder compresses and reconstructs data"
    }
    return data.get(query.lower(), "Not found")

# Call the tool once (no loop)
query_input = "capital of france"
result = search.invoke({"query": query_input})

# Print output in desired format
output = {
    "tool_used": "search",
    "input_query": query_input,
    "result": result
}

print(output)
