import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini client with API key
api_key = os.getenv("gemini_key")
if not api_key:
    raise ValueError("API key not found. Please set it in the .env file.")

client = genai.Client(api_key=api_key)

def get_gemini_response(prompt):
    """
    Function to interact with Google Gemini API using the gemini-3-flash-preview model.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    print("Fetching response from Gemini...")
    response = get_gemini_response(user_prompt)
    print("Response:", response)