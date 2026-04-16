import os
from dotenv import load_dotenv
import streamlit as st
# from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_aws import ChatBedrock

# Function to load and validate environment variables
def load_env_variables():
    load_dotenv()
    os.environ["BEDROCK_AWS_REGION"] = os.getenv("BEDROCK_AWS_REGION", "default_value")
    os.environ["BEDROCK_AWS_ACCESS_KEY_ID"] = os.getenv("BEDROCK_AWS_ACCESS_KEY_ID", "default_value")
    os.environ["BEDROCK_AWS_SECRET_ACCESS_KEY"] = os.getenv("BEDROCK_AWS_SECRET_ACCESS_KEY", "default_value")
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
    return ChatBedrock(
        region_name=os.getenv("BEDROCK_AWS_REGION"),
        aws_access_key_id=os.getenv("BEDROCK_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("BEDROCK_AWS_SECRET_ACCESS_KEY"),
        model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
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
