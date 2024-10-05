"""
Module for processing a PDF document by partitioning it into sections,
chunking the text, generating embeddings, and storing them in a vector 
store (ChromaDB).
"""

import os
import re
import argparse
from dotenv import load_dotenv
from unstructured.partition.pdf import partition_pdf
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from agenticrag.config import PERSIST_DIRECTORY, COLLECTION_NAME

# Load environment variables from a .env file
load_dotenv()


def is_section_header(element):
    """
    Check if the given element is a section header based on a specific
    pattern.

    Args:
        element: The element to check, expected to have 'category' and
        'text' attributes.

    Returns:
        bool: True if the element is a section header; otherwise, False.
    """
    pattern = r"11\.[1-5]$"
    return (element.category == 'Title' and
            re.match(pattern, element.text.split(' ')[0]))


def partition_text(elements):
    """
    Partition the text elements into sections based on section headers.

    Args:
        elements (list): List of elements parsed from the PDF.

    Returns:
        dict: A dictionary mapping section headers to their corresponding text.
    """
    partitions = {}
    current_header = None
    
    for element in elements:
        if is_section_header(element):
            current_header = element.text
            partitions[current_header] = ""
        else:
            if current_header in partitions:
                partitions[current_header] += " " + element.text

    return partitions


def chunk_documents(partitions):
    """
    Chunk the documents into smaller segments for embedding.

    Args:
        partitions (dict): A dictionary of text partitions keyed by
        section headers.

    Returns:
        list: A list of dictionaries containing chunked documents with
        metadata.
    """
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50
    )
   
    # Chunk the texts from the dictionary and store with section headers
    # as metadata
    chunked_documents = []
   
    for section, text in partitions.items():
        chunks = text_splitter.create_documents([text])
     
        # Add chunk number to metadata
        for chunk_num, chunk in enumerate(chunks):
            chunked_documents.append({
                "page_content": chunk.page_content,
                "metadata": {
                    "section": section,
                    "chunk_num": chunk_num + 1  # Make chunk numbers 1-indexed
                }
            })
  
    return chunked_documents


def embed_and_store(chunked_documents):
    """
    Generate embeddings for chunked documents and store them in a
    vector store.

    Args:
        chunked_documents (list): A list of dictionaries containing 
        chunked documents with metadata.

    Raises:
        ValueError: If the OpenAI API key is not found in environment 
        variables.
    """
    # Get the API key from the environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OpenAI API key not found in environment variables.")

    # Initialize OpenAI Embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Initialize ChromaDB (persist_directory is optional)
    vector_store = Chroma(
        embedding_function=embeddings, 
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME
    )

    # Add chunked documents to ChromaDB
    vector_store.add_texts(
        texts=[doc["page_content"] for doc in chunked_documents],
        metadatas=[doc["metadata"] for doc in chunked_documents]
    )


def process_pdf_to_vector_store(pdf_path):
    """
    Process a PDF file by parsing it, partitioning it into sections,
    chunking the text, generating embeddings, and storing them in a
    vector store.

    Args:
        pdf_path (str): The path to the PDF file to be processed.
  
    Raises:
        Exception: If an error occurs during PDF processing.
    """
    try:
        # Partition the PDF into elements
        print('Parsing pdf....', end="")
        elements = partition_pdf(
            pdf_path, 
            strategy='hi_res', 
            hi_res_model_name="detectron2_onnx"
        )
        print('Done')
        print('Partitioning text....', end="")
        partitions = partition_text(elements)
        print('Done')
        print('Chunking....', end="")
        chunked_documents = chunk_documents(partitions)
        print('Done')
        print('Embedding and vectorizing....', end="")
        embed_and_store(chunked_documents)
        print('Done')

    except Exception as e:
        raise Exception(f"An error occurred while processing the PDF: {str(e)}")


def main():
    """
    The main entry point function for the command-line tool.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process a PDF and store it in Chroma vector store.")
    parser.add_argument("pdf_path", type=str, help="The path to the PDF file to process")

    # Parse the arguments
    args = parser.parse_args()

    # Run the processing function with the provided pdf_path
    process_pdf_to_vector_store(args.pdf_path)


if __name__ == "__main__":
    main()
