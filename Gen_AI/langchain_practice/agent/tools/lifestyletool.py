from langchain.tools import tool
import aws_llm_config as aws_llm_config

llm= aws_llm_config.initialize_llm()


@tool
def lifestyle_analysis(input: str) -> str:
    """
    Evaluate lifestyle and quality of life, including work-life balance, city infrastructure, and stress factors.
    """
    print("Running lifestyle analysis tool")
    prompt = f"""
    Compare lifestyle:
    {input}

    Include:
    - Work-life balance
    - City infrastructure
    - Stress factors
    """
    return llm.invoke(prompt).content
