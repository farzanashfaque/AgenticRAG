"""
This module provides functionality to start a FastAPI backend
and a Chainlit frontend in parallel. FastAPI is started in a separate
thread, while Chainlit is started in the main thread.
"""

import subprocess
import threading


def start_fastapi():
    """
    Starts the FastAPI backend server using Uvicorn.

    This function runs the Uvicorn command to start the FastAPI
    application defined in the `app` module. The FastAPI service
    is started as a subprocess and monitored for any errors.

    Raises:
        subprocess.CalledProcessError: If the Uvicorn command fails to run.
    """
    subprocess.run(["uvicorn", "agenticrag.app:app"], check=True)


def start_chainlit():
    """
    Starts the Chainlit frontend server on port 8501.

    This function runs the Chainlit command to start the frontend
    application defined in the `app.py` file. The Chainlit service
    is started as a subprocess and monitored for any errors.

    Raises:
        subprocess.CalledProcessError: If the Chainlit command fails to run.
    """
    subprocess.run(["chainlit", "run", "agenticrag/app.py", "--port", "8501"], check=True)


def main():
    """
    Main method to start up fastapi and chainlt servers
    """
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.start()

    # Start Chainlit (blocking call, run in main thread)
    start_chainlit()


if __name__ == "__main__":
    main()
