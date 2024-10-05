import requests
import base64
import logging
from requests.exceptions import (
    HTTPError,
    Timeout,
    RequestException,
    JSONDecodeError
)
from agenticrag.config import SARVAMAI_API_KEY

# Configure logging
logging.basicConfig(level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def text_to_speech(query: str):
    """
    Converts the given text input to speech using Sarvam AI's 
    text-to-speech API.

    Args:
        query (str): The text string to convert into speech.

    Returns:
        None. The audio output is saved as a WAV file called 'output.wav'.

    Raises:
        HTTPError: If the API request returns a status code indicating failure.
        Timeout: If the API request takes too long to respond.
        ValueError: If the API response does not contain valid audio data.
        RequestException: For other issues related to the API request.
        JSONDecodeError: If the response is not valid JSON.

    Notes:
        - The function uses the Sarvam AI text-to-speech API.
        - If any error occurs during the request or audio processing, 
          it is logged, and response content is printed for debugging.
        - The audio output is saved as a WAV file named 'output.wav' 
          in the working directory.
        - A timeout of 10 seconds is applied to the API request.
    """
 
    url = 'https://api.sarvam.ai/text-to-speech'
    headers = {
        'API-Subscription-Key': SARVAMAI_API_KEY
    }
    data = {
        "inputs": [
            query
        ],
        "target_language_code": "hi-IN",
        "speaker": "meera",
        "pitch": 0.5,
        "pace": 1.2,
        "loudness": 1.5,
        "speech_sample_rate": 22050,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }

    try:
        # Set a timeout for the request
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)

        # Parse JSON response
        response_data = response.json()

        # Check if "audios" key exists in the response
        if "audios" not in response_data or not response_data["audios"]:
            raise ValueError("Invalid response: 'audios' key not found or empty.")

        base64_audio = response_data["audios"][0]

        # Decode the base64 string
        audio_data = base64.b64decode(base64_audio)

        # Save the decoded audio data as a WAV file
        with open("output.wav", "wb") as wav_file:
            wav_file.write(audio_data)

    except HTTPError as http_err:
        logging.error("HTTP error occurred: %s", http_err)
    except Timeout as timeout_err:
        logging.error("Request timed out: %s", timeout_err)
    except JSONDecodeError as json_err:
        logging.error("Failed to decode JSON response: %s", json_err)
    except ValueError as val_err:
        logging.error("Value error: %s", val_err)
    except RequestException as req_err:
        logging.error("Error during request: %s", req_err)
    finally:
        if 'response' in locals():
            print(response.content)  # Print response content in case of issues
