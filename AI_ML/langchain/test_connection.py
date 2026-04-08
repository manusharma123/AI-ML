import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

def test_azure_openai_connection():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    api_version = "2024-02-15-preview"  # ✅ Stable for chat.completions

    # ---- Validation ----
    if not endpoint or not api_key or not deployment_name:
        print("❌ Missing one of the required environment variables:")
        print("   AZURE_OPENAI_ENDPOINT")
        print("   AZURE_OPENAI_KEY")
        print("   AZURE_OPENAI_DEPLOYMENT_NAME")
        return

    # ---- Create Client ----
    client = AzureOpenAI(
        azure_endpoint=endpoint.rstrip("/"),  # ✅ normalize endpoint
        api_key=api_key,
        api_version=api_version,
    )

    try:
        response = client.chat.completions.create(
            model=deployment_name,  # ✅ MUST be deployment name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ],
            temperature=0.2,
        )

        print("✅ Connection successful!")
        print("Reply:", response.choices[0].message.content)

    except Exception as e:
        print("❌ Connection failed")
        print(type(e).__name__, ":", e)

if __name__ == "__main__":
    test_azure_openai_connection()