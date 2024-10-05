# AgenticRAG App

This is a Retrieval-Augmented Generation (RAG) based application that allows you to parse a PDF file, generate embeddings, and utilize them in an interactive application powered by FastAPI and Chainlit. The application implements a smart Agent that decides whether it's necessary to call the retrieval endpoint based on the user query. The agent can also do web searches and run Python code.

## Setup Instructions

To run this RAG application, you need to install the following dependencies:

### Required Dependencies

1. **Poppler**
   - Poppler is a PDF rendering library that is used for PDF parsing.
   - **Installation Instructions:**
     - **On Ubuntu:**
       ```bash
       sudo apt-get install poppler-utils
       ```
     - **On macOS (using Homebrew):**
       ```bash
       brew install poppler
       ```
     - **On Windows:**
       1. Download the Poppler binaries from [this link](https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.07.0-0).
       2. Extract the downloaded ZIP file to a directory (e.g., `C:\poppler`).
       3. Add the `bin` folder (e.g., `C:\poppler\poppler-<version>\bin`) to your system's PATH:
          - Right-click on `This PC` or `Computer` and select `Properties`.
          - Click on `Advanced system settings`.
          - Click on the `Environment Variables` button.
          - In the `System variables` section, find the `Path` variable and select it, then click `Edit`.
          - Click `New` and add the path to the `bin` folder.
          - Click `OK` to save and close all dialog boxes.

2. **Tesseract OCR**
   - Tesseract is an optical character recognition engine used for text extraction from images.
   - **Installation Instructions:**
     - **On Ubuntu:**
       ```bash
       sudo apt-get install tesseract-ocr
       ```
     - **On macOS (using Homebrew):**
       ```bash
       brew install tesseract
       ```
     - **On Windows:**
       1. Download the Tesseract installer from [this link](https://github.com/UB-Mannheim/tesseract/wiki).
       2. Run the installer and follow the prompts to complete the installation.
       3. Ensure that the installation directory (e.g., `C:\Program Files\Tesseract-OCR`) is added to your system's PATH using the same steps as for Poppler.

### Path Configuration

Make sure that both Poppler and Tesseract are added to your system's PATH variable. This can usually be done by adding the installation paths to your shell configuration file (like `.bashrc` or `.zshrc` for Linux/macOS).

After installation, verify that both tools are accessible from the command line by running:
```bash
pdftotext -v  # for Poppler
tesseract --version  # for Tesseract
```

### Environment Variables

Before you get started, create a `.env` file in your directory with the following content:
```
OPENAI_API_KEY=<your_openai_api_key>
SARVAMAI_API_KEY=<your_sarvamai_api_key>
```

Replace `<your_openai_api_key>` and `<your_sarvamai_api_key>` with your actual API keys.

### Cloning the Repository

Clone the repository to your local machine:

```bash
git clone <repository_url>
cd <repository_name>
```

### Configuration
In the repository, you'll find a configuration file that contains some parameters you can customize:

PERSIST_DIRECTORY - This parameter defines the location to persist the vector database.  
COLLECTION_NAME - This parameter specifies the name of the collection created to store the PDF embeddings.  
RAG_SYSTEM_PROPMPT: The system prompt for the RAG application.
Feel free to adjust these settings according to your requirements.

### Installation
Once you have your configuration set up, install the package by running:
```bash
pip install .
```

## Usage
The package has two entry points defined:

**1. Onboard PDF**: This command parses the PDF, generates embeddings, and stores them in the Chroma vector database. You can run it in your terminal as follows:
```bash
onboard_pdf "path/to/pdf"
```
**2. Start RAG App**: After onboarding your PDF, start the FastAPI and Chainlit servers by running:
```bash
start_rag_app
```
### Accessing the Application
Once the servers are up and running, you can access the Chainlit server at:
```arduino
http://localhost:8501/
```

