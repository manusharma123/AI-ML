from langchain.tools import tool
import aws_llm_config as aws_llm_config

llm= aws_llm_config.initialize_llm()

@tool
def scenario_simulator(input: str) -> str:
    """
    Simulate future scenarios and probabilities, providing best case, worst case, most likely case, and probabilities.
    """
    print("Running scenario simulator tool")
    prompt = f"""
    Simulate 3 scenarios:
    {input}

    Provide:
    - Best case
    - Worst case
    - Most likely case
    - Probabilities
    """
    return llm.invoke(prompt).content
