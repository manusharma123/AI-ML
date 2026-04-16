import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


endpoint = os.getenv("AZURE_ENDPOINT")
model_name = os.getenv("MODEL_NAME")
deployment = "pstestopenaidply-j7ytesofj2f7oa"

subscription_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("API_VERSION")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "I am going to Paris, what should I see?",
        }
    ],
    max_completion_tokens=16384,
    model=deployment
)

print(response.choices[0].message.content)