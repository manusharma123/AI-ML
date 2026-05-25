from langchain.tools import tool
import aws_llm_config as aws_llm_config

llm= aws_llm_config.initialize_llm()


@tool
def career_analysis(input: str) -> str:
    """
    Evaluate career growth prospects, including growth opportunities, skill development, and industry trends.
    """
    print("Running career analysis tool")
    prompt = f"""
    Analyze career impact:
    {input}

    Include:
    - Growth opportunities
    - Skill development
    - Industry trends
    """
    return llm.invoke(prompt).content
