import os
from dotenv import load_dotenv

load_dotenv()
print(f'OpenAI API Key exists: {bool(os.getenv("OPENAI_API_KEY"))}')
