"""
This module defines the LLM based agent and provides it access to
a RAG tool to retrieve information on specific topics.
"""
import os
import requests
from langchain.tools import Tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from requests.exceptions import Timeout, ConnectionError, HTTPError
from agenticrag.config import OPENAI_API_KEY

# Set the OpenAI API key as an environment variable
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


def call_rag_system(question: str) -> str:
    """
    Calls the Retrieval-Augmented Generation (RAG) system with a provided 
    question.

    This function sends a POST request to the RAG endpoint and retrieves the
    answer for the specified question. It handles various errors, including
    timeouts, connection issues, and HTTP errors, returning appropriate
    error messages when necessary.

    Args:
        question (str): The question to be sent to the RAG system.

    Returns:
        str: The answer retrieved from the RAG system or an error message 
        if the call fails.
    """
    try:
        print('entered rag tool')
        response = requests.post(
            "http://127.0.0.1:8000/rag",
            json={"question": question},
            timeout=5  # Set a timeout of 5 seconds
        )
        print('got response')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json().get("answer", "No answer returned from RAG")
    except Timeout:
        return "Error: The request to the RAG system timed out."
    except ConnectionError:
        return "Error: Failed to connect to the RAG system. Check if it's running."
    except HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as e:
        return f"Error calling RAG system: {str(e)}"


def create_agent():
    """
    Creates and returns a React agent that uses the RAG system for 
    answering questions.

    This function defines a tool that interfaces with the RAG system, 
    initializes a language model using the OpenAI API, and sets up a 
    memory saver for the agent. The agent can use the RAG system to 
    answer questions based on retrieved context.

    Returns:
        Agent: A React agent configured with the RAG system tool and 
        language model for processing queries.
    """
    # Define a Tool for the RAG system
    rag_tool = Tool.from_function(
        func=call_rag_system,
        name="RAG_System",
        description="Searches and returns excerpts from the NCERT physics "
                    "chapter on sound."
    )

    # List of tools for the agent (RAG system and general LLM)
    tools = [rag_tool]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    memory = MemorySaver()

    # Create the agent using the language model, tools, and memory saver
    agent = create_react_agent(llm, tools, checkpointer=memory)
    return agent
