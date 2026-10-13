import os
from dotenv import load_dotenv
import google.genai as genai

# Load variables from .env into environment
load_dotenv()

# Get the API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure the client
client = genai.Client(api_key=api_key)

# Make a request to Gemini
response = client.models.generate_content(
    model="gemini-2.5-flash",  # or "gemini-1.5-pro"
    contents="What is the weather in New Delhi on 10th sep 2025"
)

# Print the model output
print(response.text)