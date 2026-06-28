import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
print(f"API Key read: {api_key[:10] if api_key else 'None'}...")
print(f"API Key starts with AIzaSy: {api_key.startswith('AIzaSy') if api_key else False}")

try:
    from google import genai
    print("google-genai library imported successfully.")
    client = genai.Client(api_key=api_key)
    print("genai.Client initialized. Testing generate_content...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Hello, reply with one word: Success"
    )
    print(f"Response text: {response.text}")
except Exception as e:
    print(f"Error occurred: {str(e)}")
