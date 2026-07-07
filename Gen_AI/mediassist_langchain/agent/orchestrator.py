from pydoc import doc
from .general_chatagent.general_agent import research
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from rich import print
import config.llm_config as az_llm_config
import db.db_config as db_config
from agent.agent_helpers.agent_memory import create_session_id, check_User_session_exists_update_history
from agent.agent_helpers.helpers import safe_agent_invoke
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


default_system_instruction = """
you are a trained medical intake assistant.

Your job is to gather detailed patient symptoms through a conversational approach.

Guidelines/restructions:
- Ask 3 - 5 questions to analyse the symtems and gather relevant information
- Ask ONE question at a time
- Be empathetic and supportive
- Collect:
  • Primary symptoms
  • Duration (when started)
  • Severity (mild/moderate/severe)
  • Associated symptoms
  • Age and gender
  • Existing conditions (diabetes, BP, etc.)
  • Medications currently taken

Important:
- DO NOT provide diagnosis
- DO NOT give treatment
- Response only with questions to gather information, never provide any suggestions or recommendations
- Keep asking until enough detail is gathered

If sufficient data is collected call appropriate tool/ sub-agent to summarize and gather little info about symptom in a structured paragraph.

Conversation:
User: {query}
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
        model = az_llm_config.initialize_llm(),
        tools=[research]
    )
    message_with_history = db_config.get_all_history_by_session_id(os.getenv("HISTORY_COLLECTION"), session_id=session_id)
    if message_with_history:
        print(f"Found history for session_id {session_id}: {message_with_history}")
    else:
        message_with_history = ""

    # search_agent = build_search_agent()
    search_result = safe_agent_invoke(main_agent, {
        "messages": [
            SystemMessage(content=default_system_instruction),
            HumanMessage(content=f"{message_with_history},{topic}")]
    }, 3)
    state["search_results"] = search_result['messages'][-1].content
    state["Metadata"] = search_result['messages'][-1].response_metadata
    print("\n bot : ", state['search_results'])
    
    # Print only prompt, completion and total token counts from metadata
    meta = state.get("Metadata", {})
    token_usage = meta.get("token_usage", {}) if isinstance(meta, dict) else {}
    prompt_tokens = token_usage.get("prompt_tokens")
    completion_tokens = token_usage.get("completion_tokens")
    total_tokens = token_usage.get("total_tokens")
    print(f"prompt_tokens: {prompt_tokens}, completion_tokens: {completion_tokens}, total_tokens: {total_tokens}")
    
    #save search result to history and update in db
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