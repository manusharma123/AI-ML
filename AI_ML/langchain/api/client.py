import requests 
import streamlit as st

def get_openai_response(user_input):
    response= requests.post("http://localhost:8001/poem/invoke", json={'input':{'query':user_input}})
    return response.json()['output']['content']


st.title("LangChain Bedrock API Client")
user_input = st.text_input("Enter your query:")
if user_input:
    response = get_openai_response(user_input)
    st.write(response)