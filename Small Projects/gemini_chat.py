import os
from dotenv import load_dotenv
import google.generativeai as genai  # ✅ correct import

# Load variables from .env into environment
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key exists
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure the genai client with your API key
genai.configure(api_key=api_key)

# Create a GenerativeModel instance
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"

# Generate content using a prompt
response = model.generate_content("What is 2 + 8?")

# Print the model's response
print(response.text)
