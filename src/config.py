import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN not set in .env")

# Pick a reasonably small instruction model
# You can change this later to any chat/instruction model you prefer.
HF_MODEL = "meta-llama/Llama-3.1-8B-Instruct" # example

client = InferenceClient(
    model=HF_MODEL,
    token=HF_TOKEN,
)