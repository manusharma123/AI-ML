from pydoc import doc

from agent.chat_agent import build_search_agent, build_analysis_agent
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from rich import print
import aws_llm_config as aws_llm_config
import db_config
from agent.agent_memory import create_session_id, check_User_session_exists_update_history

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


default_system_instruction = """
you are my personal assistant that provides helpful information by doing web searches. Only use relevant tools according to the human message.
you also have a chat history of the conversation which you can refer to for context. Always provide a final answer to the human after using the tools, and make sure to use the most relevant tool for each question.
also found on the last question the user asked.
"""
system_instruction = """
Based on all analyses, provide:
1. Report summary
2. Recommendation (Yes/No/Conditional)
3. Confidence score (0-100%)
4. Key risks
5. Final reasoning
Note :  you are a general purpose  assistant that provides helpful information by doing web searches or analysis. Only use relevant tools according to the human message.
"""

history = []

def run_research_pipeline(topic: str, session_id: str, user: str) -> dict:
    state = {}
    config = {"configurable": {"session_id": session_id}}
    history.append({"role": "user", "content": topic})

    # search agent working
    print("\n" + " =" * 50)
    print("Deepsearch agent is working ...")
    print("=" * 50)
    main_agent = create_agent(
        model = aws_llm_config.initialize_llm(),
        tools=[build_search_agent, build_analysis_agent]
    )
    message_with_history = db_config.get_all_history_by_session_id(os.getenv("HISTORY_COLLECTION"), session_id=session_id)
    if message_with_history:
        print(f"Found history for session_id {session_id}: {message_with_history}")
    else:
        message_with_history = "ignore no history found for this session"

    # search_agent = build_search_agent()
    search_result = main_agent.invoke({
        "messages": [
            SystemMessage(content=system_instruction),
            HumanMessage(content=f"{message_with_history},{topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content

    # print("\n user : ", search_result['messages'][1].content)
    print("\n bot : ", state['search_results'])
    history.append({"role": "bot", "content": state['search_results']})
    doc={"session_id": session_id, "user": user, "history": history}
    check_User_session_exists_update_history(os.getenv("HISTORY_COLLECTION"), doc) # check if session exists for user and update history, if not create new document with session id and history

    

    return state


if __name__ == "__main__":
    user = "sumitsha"
    session_id = db_config.get_all_session_ids(os.getenv("HISTORY_COLLECTION"))
    # doc={"session_id": session_id, "user": user, "history": "history"}
    # check_session_exists_for_user(os.getenv("HISTORY_COLLECTION"), doc)
    if session_id == []:
        session_id = create_session_id()
    else:
        print(f"Resuming with existing session_id: {session_id}")
        session_id = input('Press Enter to existing session id or type "new" to start a new session: ')
    while True:
        if session_id.lower() == "new":
            session_id = create_session_id()
            print(f"Starting new session with session_id: {session_id}")
        else:
            print(f"Starting session with session_id: {session_id}")
        topic = input("\n Enter a research topic (or type 'exit' to quit): ")
        if topic.lower() == 'exit':
            break
        run_research_pipeline(topic, session_id, user)