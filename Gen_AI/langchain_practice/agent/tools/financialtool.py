from langchain.tools import tool
import aws_llm_config as aws_llm_config

llm= aws_llm_config.initialize_llm()


@tool
def finance_analysis(input: str) -> str:
    """
    Analyze financial impact of a decision, including salary difference, cost of living, and savings projection.
    """
    print("Running finance analysis tool")
    prompt = f"""
    Analyze financial impact:
    {input}

    Include:
    - Salary difference
    - Cost of living
    - Savings projection
    """
    return llm.invoke(prompt).content
