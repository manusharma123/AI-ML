from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from agent.utils import initialize_llm
import os
import logging

# Add logging to debug the retriever output
logging.basicConfig(level=logging.DEBUG)

def load_wizard_of_oz():
    # Update the file path to use an absolute path
    loader = TextLoader(os.path.join(os.path.dirname(__file__), "WIZARD_OF_OZ.txt"), encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)


def build_vectorstore():
    docs = load_wizard_of_oz()

    embeddings = AzureOpenAIEmbeddings(
        model = os.getenv("TEXT_EMBEDDING_MODEL"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version=os.getenv("EMBEDDING_API_VERSION"),
        deployment=os.getenv("EMBEDDING_DEPLOYMENT_NAME")
    )

    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


def get_retriever():
    vectorstore = build_vectorstore()
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )



rag_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an intelligent assistant. Answer ONLY using the provided context. "
        "If the answer is not in the context, say 'I could not find that in the provided document.'"
    ),
    (
        "human",
        """Context:
{context}

Question:
{question}"""
    )
])


def build_rag_chain():
    retriever = get_retriever()
    llm = initialize_llm()

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    return (
        RunnablePassthrough()              # <-- receives STRING
        | {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    )