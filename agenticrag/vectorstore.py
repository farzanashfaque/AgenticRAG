"""
This module initializes the necessary components for building a Retrieval-based
Question Answering (QA) system using the LangChain framework.
"""
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from agenticrag.config import OPENAI_API_KEY, PERSIST_DIRECTORY, COLLECTION_NAME


def initialize_vectorstore():
    """
    Initializes and returns a Chroma vector store for document embeddings
    and retrieval.

    This function performs the following steps:
    1. Initializes OpenAI embeddings using the provided API key.
    2. Initializes a Chroma vector store that uses these embeddings for storing
       and retrieving documents based on their vector representations.
       The vector store is persisted in a specified directory and grouped
       by a collection name.

    Returns:
        Chroma: A Chroma vector store object for embedding-based
                document retrieval.
    """
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    # Initialize Chroma vector store
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME
    )
    return vector_store
