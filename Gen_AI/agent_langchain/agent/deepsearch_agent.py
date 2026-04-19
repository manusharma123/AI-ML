from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from agent.deepsearch import web_search
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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
    return create_agent(
        model = initialize_llm(),
        tools= [web_search]
    )

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Your goal is to produce clear, structured, and insightful reports that adhere to the highest standards of accuracy, ethics, and professionalism. Always prioritize factual accuracy, transparency in methodology, and ethical considerations when presenting information."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Methodology (explain how sources were selected, weighted, and verified; include any limitations or biases in the data)
- Ethical Considerations (highlight any ethical concerns, such as privacy, bias, or misinformation risks, and how they were addressed)
- Primary Documents (quote or attach key documents like notifications, FIRs, etc.)
- Conclusion
- Sources (list all URLs found in the research, with timestamps and retrieval details)

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