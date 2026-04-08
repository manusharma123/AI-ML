import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Function to load and validate environment variables
def load_env_variables():
    load_dotenv()
    os.environ["AZURE_OPENAI_KEY"] = os.getenv("AZURE_OPENAI_KEY", "default_value")
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT", "default_value")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "default_value")

# Function to create the LangChain prompt template
def create_prompt_template():
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Please respond to the user queries."),
            ("user", "Question:{question}")
        ]
    )

# Function to initialize the Azure OpenAI LLM
def initialize_llm():
    return AzureChatOpenAI(
        azure_deployment="gpt-5-mini",
        api_version="2025-08-07",
        temperature=0.9,
        timeout=None
    )

# Main function to run the Streamlit app
def main():
    load_env_variables()

    # Streamlit app UI
    st.title("LangChain OpenAI Chat Example")
    user_input = st.text_input("Enter your question:")

    if user_input:
        # Initialize components
        prompt = create_prompt_template()
        llm = initialize_llm()
        output_parser = StrOutputParser()

        # Create the chain
        chain = prompt | llm | output_parser

        # Generate and display the response
        try:
            response = chain.invoke({"question": user_input})
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
