from agent.deepsearch_agent import build_search_agent, writer_chain, critic_chain
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from agent.memory import get_session_history
from rich import print


store={}
config = {"configurable": {"session_id": "chat1"}}

def run_research_pipeline(topic: str) -> dict:
    state = {}

    # search agent working
    print("\n" + " =" * 50)
    print("Deepsearch agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [
            SystemMessage(content="you are my personal assistant that provides helpful information by doing web searches."),
            HumanMessage(content=f"{topic}")]
    },config=config)
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ", state['search_results'])

    # writer chain
    # print("\n" + " =" * 50)
    # print("Generating Report: In progress ...")
    # print("=" * 50)

    research = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
    )
    # with_message_history = RunnableWithMessageHistory(writer_chain, get_session_history, input_messages_key="topic")
    
    # config = {"configurable":{"session_id": "chat1"}}
    # state["report"] = writer_chain.invoke({
    #     "topic": topic,
    #     "research": research
    # })

    # print("\n Final Report\n", state["report"])

    #critic report 

    # print("\n"+" ="*50)
    # print("step 3 - critic is reviewing the report ")
    # print("="*50)

    # state["feedback"] = critic_chain.invoke({
    #     "report":state['report']
    # })

    # print("\n critic report \n", state['feedback'])

    return state

if __name__ == "__main__":
    while True:
        topic = input("\n Enter a research topic (or type 'exit' to quit): ")
        if topic.lower() == 'exit':
            print("Exiting the session. Goodbye!")
            break
        run_research_pipeline(topic)
