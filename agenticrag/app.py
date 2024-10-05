from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
import chainlit as cl
import requests
from requests.exceptions import Timeout
from agenticrag.retrieval_chain import create_qa_chain
from agenticrag.agent import create_agent
from agenticrag.config import RAG_SYSTEM_PROMPT
from agenticrag.sarvam import text_to_speech

# Initialize the QA Chain
qa_chain = create_qa_chain()
# Initialize agent
agent = create_agent()


class Query(BaseModel):
    """Model representing a query with a question string."""
    question: str


app = FastAPI()


@cl.on_chat_start
async def start_chat():
    """Send a welcome message when the chat starts."""
    await cl.Message("Welcome to the RAG Agent! Ask me anything about sound.").send()


@cl.on_message
async def handle_message(message: str):
    """
    Handle incoming messages from the chat and forward them to the agent.

    Args:
        message (str): The user's message to be processed by the agent.
    """
    try:
        # Send the user's message to the /agent endpoint with a timeout
        response = requests.post(
            "http://127.0.0.1:8000/agent",
            json={"question": message.content},
            timeout=5  # Set a timeout of 5 seconds
        )
        response.raise_for_status()  # Raise an error for bad responses
    
        answer = response.json().get("answer", "No answer returned from agent.")
        text_to_speech(answer[:500])  # Limit to first 500 characters
    
        elements = [cl.Audio(name="audio", path="./output.wav", display="inline")]
        await cl.Message(content=f"Agent: {answer}", elements=elements).send()
    
    except Timeout:
        await cl.Message("Error: The request to the agent timed out.").send()
    except requests.exceptions.RequestException as req_err:
        await cl.Message(f"Error: {req_err}").send()
    except Exception as e:
        await cl.Message(f"An unexpected error occurred: {str(e)}").send()


@app.post("/rag")
def ask_question(query: Query):
    """
    Endpoint for asking a question to the RAG system.

    Args:
        query (Query): A query object containing the user's question.

    Returns:
        dict: A dictionary containing the answer from the QA chain.

    Raises:
        HTTPException: If an error occurs while processing the question.
    """
    full_prompt = f"{RAG_SYSTEM_PROMPT}\n\nHuman: {query.question}\nAssistant:"
    try:
        # Run the QA chain with the provided question
        result = qa_chain.run(query.question)
        return {"answer": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent")
def agent_endpoint(query: Query):
    """
    Endpoint for interacting with the agent.

    Args:
        query (Query): A query object containing the user's question.

    Returns:
        dict: A dictionary containing the answer from the agent.

    Raises:
        HTTPException: If an error occurs while processing the question.
    """
    try:
        config = {"configurable": {"thread_id": "abc123"}}
        events = []

        for event in agent.stream(
            {"messages": [HumanMessage(content=query.question)]},
            config=config,
            stream_mode="values",
        ):
            print(event["messages"][-1].content)
            events.append(event)

        result = events[-1]["messages"][-1].content
        return {"answer": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
