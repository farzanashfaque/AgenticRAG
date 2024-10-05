"""
This module sets up a question-answering (QA) system using a language model
(LLM) with conversational memory and retrieval capabilities from a vector
store.
"""

from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from agenticrag.vectorstore import initialize_vectorstore
from agenticrag.config import OPENAI_API_KEY


def create_qa_chain():
    """
    Initializes and returns a question-answering (QA) chain using a language
    model (LLM) with conversational memory and retrieval capabilities from a
    vector store.

    This function performs the following steps:
    1. Initializes an OpenAI LLM instance with the provided API key.
    2. Initializes a memory buffer to store conversation history
       (using `ConversationBufferMemory`).
    3. Initializes a vector store for storing and retrieving relevant
       documents.
    4. Creates a RetrievalQA chain that uses the LLM to answer questions by
       retrieving relevant documents from the vector store. The memory buffer
       ensures that the conversation context is retained between interactions.

    Returns:
        RetrievalQA: A QA chain object that can be used to ask questions and
        retrieve answers based on the stored conversation and vector store 
        information.
    """
    # Initialize the LLM
    llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    # Initialize memory
    memory = ConversationBufferMemory()
    # Initialize vector store
    vector_store = initialize_vectorstore()
    # Create RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return qa_chain
