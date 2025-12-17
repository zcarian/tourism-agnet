"""
Configuration module for the Tourism Projections Extractor.

This module handles:
- Loading environment variables from a .env file
- Setting up the Hugging Face Inference API client
- Configuring the LLM model to use for document analysis

Required Environment Variables:
    HF_TOKEN: Your Hugging Face API token (get one at https://huggingface.co/settings/tokens)
"""

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError(
        "HF_TOKEN not set in .env file. "
        "Please create a .env file with your Hugging Face token. "
        "Get your token at: https://huggingface.co/settings/tokens"
    )

HF_MODEL = "meta-llama/Llama-3.1-8B-Instruct"

client = InferenceClient(
    model=HF_MODEL,
    token=HF_TOKEN,
)
