
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
import os
from agent.agent_helpers.tools.web_search import web_search
from config.llm_config import initialize_llm
from langchain.tools import tool
from .General_Prompt import GENERAL_SYSTEM_PROMPT
from agent.agent_helpers.helpers import safe_agent_invoke

# Load environment variables
load_dotenv()


def create_prompt_template():
    """Create chat prompt"""
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("user", "{question}")
        ]
    )

@tool("medical_research", description="You are an agent that only handles medical related queries and provides information by doing web search. Only use this tool when the user query is related to a medical symptoms.")
def research(query: str):
    print(f"Building search agent")
    subagent = create_agent(
        model = initialize_llm(),
        tools=[web_search],
    )
    
    result = safe_agent_invoke(subagent, {
        "messages": [
            {"role": "system", "content": GENERAL_SYSTEM_PROMPT},
            {"role": "user", "content": query}]
    })

    return result["messages"][-1].content



# @tool("analysis", description="Analyze a career and lifestyle related topic and return report")
# def build_analysis_agent(query: str):
#     print("Building analysis agent")
#     agent = create_agent(
#         model = az_llm_config.initialize_llm(),
#         tools=[lifestyle_analysis, career_analysis, finance_analysis, scenario_simulator],
#     )
    
#     result = agent.invoke({
#         "messages": [{"role": "user", "content": query}]
#     })

#     return result["messages"][-1].content
