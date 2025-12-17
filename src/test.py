from config import client


def main():
    print("Calling Hugging Face Inference API...")

    messages = [
        {"role": "system", "content": "You MUST respond with EXACTLY what the user requests — no extra text, no explanations."},
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