from langchain_openai import AzureChatOpenAI
import os

def initialize_llm():
    """Initialize Azure OpenAI Chat Model"""
    return AzureChatOpenAI(
        model=os.getenv("MODEL_NAME"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version=os.getenv("API_VERSION"),
        deployment_name=os.getenv("DEPLOYMENT_NAME"),
        temperature=0.7
    )