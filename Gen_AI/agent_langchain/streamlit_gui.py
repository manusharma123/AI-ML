import streamlit as st
from pipeline import run_research_pipeline, rag_pipeline

def main():
    st.title("Weather Assistant GUI")

    # Research Pipeline Section
    st.header("Research Pipeline")
    topic = st.text_input("Enter a research topic:")
    if st.button("Run Research Pipeline"):
        if topic:
            with st.spinner("Running research pipeline..."):
                result = run_research_pipeline(topic)
            st.success("Research pipeline completed!")
            st.subheader("Search Results:")
            st.write(result.get("search_results", "No results found."))
        else:
            st.error("Please enter a research topic.")

    # RAG Pipeline Section
    st.header("RAG Pipeline")
    question = st.text_input("Enter a question for the RAG chatbot:")
    if st.button("Run RAG Pipeline"):
        if question:
            with st.spinner("Running RAG pipeline..."):
                answer = rag_pipeline(question)
            st.success("RAG pipeline completed!")
            st.subheader("Answer:")
            st.write(answer.get("answer", "No answer found."))
        else:
            st.error("Please enter a question.")

if __name__ == "__main__":
    main()