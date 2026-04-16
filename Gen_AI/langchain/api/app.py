from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["AWS_REGION"] = os.getenv("BEDROCK_AWS_REGION")
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("BEDROCK_AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("BEDROCK_AWS_SECRET_ACCESS_KEY")

app = FastAPI(
    title="LangChain Bedrock API",
    description="API for interacting with AWS Bedrock using LangChain",
    version="1.0.0",
)

model = ChatBedrock(
    model="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    temperature=0.2,
)

add_routes(app, model, path="/bedrock")

prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant. Please respond to the user query in simple words:\n{query}"
)

chain = prompt | model
add_routes(app, chain, path="/poem")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)