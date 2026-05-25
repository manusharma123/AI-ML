
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
import os
from agent import agent_memory
from agent.tools.deepsearchtool import web_search
from agent.tools.lifestyletool import lifestyle_analysis
from agent.tools.employementtool import career_analysis
from agent.tools.financialtool import finance_analysis
from agent.tools.scienarioSimulationtool import scenario_simulator

import aws_llm_config as aws_llm_config
from langchain.tools import tool
from langchain_core.runnables.history import RunnableWithMessageHistory

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

@tool("research", description="Research a topic from web and return findings")
def build_search_agent(query: str):
    print(f"Building search agent : {query}")
    subagent = create_agent(
        model = aws_llm_config.initialize_llm(),
        tools=[web_search],
    )
    
    result = subagent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    return result["messages"][-1].content



@tool("analysis", description="Analyze a career and lifestyle related topic and return report")
def build_analysis_agent(query: str):
    print("Building analysis agent")
    agent = create_agent(
        model = aws_llm_config.initialize_llm(),
        tools=[lifestyle_analysis, career_analysis, finance_analysis, scenario_simulator],
    )
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    return result["messages"][-1].content
