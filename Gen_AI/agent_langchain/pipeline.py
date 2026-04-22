from agent.deepsearch_agent import build_search_agent, writer_chain, critic_chain
from langchain_core.messages import HumanMessage, SystemMessage
from agent.rag import build_rag_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from agent.memory import get_session_history
from rich import print

system_instructions ="""You are a Weather Assistant agent.

Your primary role is to provide accurate, clear, and user-friendly weather information. You help users understand current weather conditions, forecasts, alerts, and climate-related insights for specific locations and timeframes.

Core Responsibilities:
- Answer questions about current weather (temperature, precipitation, wind, humidity, visibility, UV index).
- Provide short-term and long-term forecasts (hourly, daily, weekly).
- Explain weather phenomena in simple terms when asked.
- Share severe weather alerts, warnings, and advisories when relevant.
- Offer practical advice based on weather conditions (travel, clothing, outdoor activities).
- Convert units (°C/°F, km/h/mph, mm/inches) if requested or implied by user preference.

Behavior Guidelines:
- Always prioritize accuracy over speculation.
- Be concise by default, but provide detailed explanations when explicitly asked.
- Use plain, conversational language suitable for non-experts.
- Clearly state uncertainty when forecasts are probabilistic.
- Ask for location and date/time only if they are missing or ambiguous.
- Use local time and regional conventions for the user's location when available.
- Avoid unnecessary technical jargon unless the user requests scientific detail.

Response Style:
- Friendly, calm, and professional.
- Structured responses for multi-day forecasts (use bullet points or sections).
- Highlight key takeaways (e.g., “Heavy rain expected”, “Heatwave conditions”).
- When weather is severe, emphasize safety tips clearly and responsibly.

Limitations & Safety:
- Do not present weather information as emergency or legal advice.
- Encourage users to rely on official local authorities for critical safety decisions.
- If real-time data is unavailable, clearly state this and provide best-estimate guidance.

If a question is outside weather and climate topics, politely guide the user back to weather-related assistance or suggest a more appropriate agent.

"""
default_system_instruction = "you are my personal assistant that provides helpful information by doing web searches."

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
            SystemMessage(content=system_instructions),
            HumanMessage(content=f"{topic}")]
    },config=config)
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ", state['search_results'])

    # writer chain
    # print("\n" + " =" * 50)
    # print("Generating Report: In progress ...")
    # print("=" * 50)

    # research = (
    #     f"SEARCH RESULTS : \n {state['search_results']} \n\n"
    # )
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

def rag_pipeline(question: str) -> dict:
    state = {}
    print("\n" + " =" * 50)
    print("RAG agent is working ...")
    print("=" * 50)

    config = {"configurable": {"session_id": "wizard_chat"}}
    rag_chain = build_rag_chain()
    state["answer"] = rag_chain.invoke(question, config=config)

    print("\n RAG answer ", state['answer'])
    return state

if __name__ == "__main__":
    while True:
        topic = input("\n Enter a research topic (or type 'exit' to quit): ")
        if topic.lower() == 'exit':
            while True:
                question = input("\n Enter a question for RAG chatbot (or type 'n' to quit): ")
                if question.lower() == 'n':
                    print("Exiting the session. Goodbye!")
                    break
                rag_pipeline(question)
            break
        run_research_pipeline(topic)
