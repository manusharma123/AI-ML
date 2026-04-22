from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from agent.deepsearch import web_search
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from agent.memory import get_session_history
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


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

def create_prompt_template():
    """Create chat prompt"""
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("user", "{question}")
        ]
    )

def build_search_agent():
    agent = create_agent(
        model = initialize_llm(),
        tools= [web_search]
    )
    return RunnableWithMessageHistory(
        agent,
        get_session_history,
        input_messages_key="messages"
    )


writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a weather assistant which provide only weather related information to user. Your goal is to produce clear, structured, and insightful reports that adhere to the highest standards of accuracy, ethics, and professionalism."),
    ("human", """Write a detailed research report on the topic below.use the provided research gathered only if its relevant to the topic.

Topic: {topic}

Research Gathered:
{research}

Be detailed, factual, and professional. Highlight causal relationships, provide alternative explanations where applicable, and ensure transparency in your reasoning."""),
])

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Your role is to evaluate reports with honesty, precision, and adherence to ethical standards. Always assess the report’s accuracy, transparency, and ethical integrity, and provide actionable recommendations for improvement."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

Ethical Considerations:
- Highlight any ethical concerns (e.g., privacy, bias, misinformation risks) and whether they were addressed adequately.

Specific Recommendations:
- ...
- ...

One line verdict:
..."""), 
])

writer_chain = writer_prompt | initialize_llm() | StrOutputParser()
critic_chain = critic_prompt | initialize_llm() | StrOutputParser()



def call_agent():
    user_input = input("Enter your question: ")

    if not user_input.strip():
        print("Please enter a valid question.")
        return

    try:
        # Initialize components
        prompt = create_prompt_template()
        llm = initialize_llm()
        output_parser = StrOutputParser()

        # Build chain
        chain = prompt | llm | output_parser

        # Invoke chain
        response = chain.invoke({"question": user_input})
        print("\nResponse:\n")
        print(response)

    except Exception as e:
        print(f"An error occurred: {e}")

# if __name__ == "__main__":
# call_agent()