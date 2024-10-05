# AgenticRAG App

This is a Retrieval-Augmented Generation (RAG) based application that allows you to parse a PDF file, generate embeddings, and utilize them in an interactive application powered by FastAPI and Chainlit. The application implements a smart Agent that decides based on the user query whether its necessary to call the retrieval endpoint.

## Setup Instructions

### Environment Variables

Before you get started, create a `.env` file in your directory with the following content:
`
OPENAI_API_KEY=<your_openai_api_key> 
SARVAMAI_API_KEY=<your_sarvamai_api_key>
`

Replace `<your_openai_api_key>` and `<your_sarvamai_api_key>` with your actual API keys.

### Cloning the Repository

Clone the repository to your local machine:

```bash
git clone <repository_url>
cd <repository_name>
```

### Configuration
In the repository, you'll find a configuration file that contains some parameters you can customize:

PERSIST_DIRECTORY: This parameter defines the location to persist the vector database.
COLLECTION_NAME: This parameter specifies the name of the collection created to store the PDF embeddings.
System Prompt: The system prompt for the RAG application.
Feel free to adjust these settings according to your requirements.

### Installation
Once you have your configuration set up, install the package by running:
```bash
pip install .
```

## Usage
The package has two entry points defined:

1. Onboard PDF: This command parses the PDF, generates embeddings, and stores them in the Chroma vector database. You can run it in your terminal as follows:
```bash
onboard_pdf "path/to/pdf"
```
2. Start RAG App: After onboarding your PDF, start the FastAPI and Chainlit servers by running:
```bash
start_rag_app
```
### Accessing the Application
Once the servers are up and running, you can access the Chainlit server at:
```arduino
http://localhost:8501/
```



