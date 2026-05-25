from langchain_openai import AzureChatOpenAI
import os

def initialize_llm():
    """Initialize Azure OpenAI Chat Model"""
    required_vars = [
        "AZURE_OPENAI_MODEL",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
        "DEPLOYMENT_NAME"
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    return AzureChatOpenAI(
        model=os.getenv("AZURE_OPENAI_MODEL"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        deployment_name=os.getenv("DEPLOYMENT_NAME"),
        temperature=0.7
    )