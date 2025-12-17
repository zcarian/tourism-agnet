"""
Test module for verifying Hugging Face API connection.

Run this script to check that your HF_TOKEN is valid and the
inference API is working correctly.

Usage:
    python src/test.py

Expected output:
    "tourism agent HF OK"
"""

from config import client


def main():
    """
    Test the Hugging Face Inference API connection.
    
    Sends a simple prompt to verify:
    1. The API token is valid
    2. The model is accessible
    3. Responses are being received correctly
    """
    print("Calling Hugging Face Inference API...")

    messages = [
        {"role": "system", "content": "You MUST respond with EXACTLY what the user requests - no extra text, no explanations."},
        {"role": "user", "content": "Respond with EXACTLY: tourism agent HF OK"},
    ]

    response = client.chat_completion(
        messages=messages,
        max_tokens=20,
        temperature=0.0,
    )

    print("Raw response:", response)
    print("Answer:", response.choices[0].message["content"])


if __name__ == "__main__":
    main()
