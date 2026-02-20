import os
from google import genai
from dotenv import load_dotenv

# Import the system prompt we just created
try:
    from app.core.prompts import SYSTEM_PROMPT
except ImportError:
    # Fallback for direct script execution without package structure
    from prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()


def get_gemini_client():
    """
    Returns a configured google-genai Client.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    return genai.Client(api_key=api_key)


def get_model_name():
    """
    Returns the preferred model name.
    """
    return "gemini-2.0-flash"  # Using the latest stable flash model


def get_generation_config():
    """
    Returns the default generation configuration.
    """
    return {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "system_instruction": SYSTEM_PROMPT,
    }


if __name__ == "__main__":
    try:
        client = get_gemini_client()
        model_name = get_model_name()
        print("Gemini client configured successfully.")
        print(f"Client initialized: {type(client).__name__}")
        print(f"Model Name: {model_name}")
        print(f"System Prompt Length: {len(SYSTEM_PROMPT)} characters")
    except Exception as e:
        print(f"Setup failed: {e}")
