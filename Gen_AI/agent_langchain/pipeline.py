from agent.deepsearch_agent import  build_search_agent , writer_chain , critic_chain
from rich import print
def run_research_pipeline(topic : str) -> dict:

    state = {}

    #search agent working 
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    # print("\n search agent output \n", search_result)
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ",state['search_results'])

    #step 3 - writer chain 

    print("\n"+" ="*50)
    print("step 2 - Writer is drafting the report ...")
    print("="*50)

    research = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research
    })

    print("\n Final Report\n",state['report'])

    #critic report 

    print("\n"+" ="*50)
    print("step 3 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
