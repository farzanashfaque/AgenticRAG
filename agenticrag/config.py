"""
This module loads API keys and configurations for use in the question-answering
system and defines the system prompt for retrieval-augmented generation (RAG).
"""
import os
from dotenv import load_dotenv

# Load the .env file that contains your API key
load_dotenv()

# Fetch API keys and other configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SARVAMAI_API_KEY = os.getenv("SARVAMAI_API_KEY")
PERSIST_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "NCERT_CHAPTER_11_SOUND"
RAG_TOPIC = "Sound"

# Define the system prompt for RAG
RAG_SYSTEM_PROMPT = (
    "You are a knowledgeable assistant in the field of physics. "
    "Answer all questions on the topic of sound only based on the context retrieved. "
    "Do not use your existing knowledge. "
    "I repeat: DO NOT USE YOUR EXISTING KNOWLEDGE TO ANSWER QUESTIONS ON THE TOPIC OF SOUND. "
    "If the context is not sufficient, say you don't have sufficient information."
)
