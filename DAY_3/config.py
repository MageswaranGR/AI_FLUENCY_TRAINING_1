import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
MODEL=os.getenv("MODEL","qwen2.5:1.5b")
client=OpenAI(base_url="http://localhost:11434/v1",api_key="ollama")
def banner(title):
 print("="*70); print(title); print(f"MODEL: {MODEL}"); print("="*70)