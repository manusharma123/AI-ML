
import os
from openai import AzureOpenAI
import dotenv 

# Load environment variables from .env file
dotenv.load_dotenv()

# User-friendly: Read sensitive info from environment variables
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://pstestopenaidply-mp3wuiuejkox2a.openai.azure.com/")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "pstestopenaidply-mp3wuiuejkox2a")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
subscription_key = os.getenv("AZURE_OPENAI_KEY")  # Must be set in environment

def main():
    if not subscription_key:
        print("Error: Please set the AZURE_OPENAI_KEY environment variable for your API key.")
        return

    user_input = input("Ask the assistant anything: ")

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_completion_tokens=1024,
            model=deployment
        )
        print("\nAssistant:", response.choices[0].message.content)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()