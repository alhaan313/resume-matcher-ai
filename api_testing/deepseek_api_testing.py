import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

messages = [
    {"role": "user", "content": "What is the capital of France?"}
]

def test_provider(name, model_name, api_key=None):
    print(f"\nTesting provider: {name}")
    try:
        client = InferenceClient(provider=name, api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=100
        )
        print(f"✅ {name} response: {response.choices[0].message['content']}")
    except Exception as e:
        print(f"❌ {name} failed: {e}")

if __name__ == "__main__":
    test_provider("together", "deepseek-ai/DeepSeek-R1", os.getenv("TOGETHER_DEEPSEEK_KEY"))
    test_provider("sambanova", "deepseek-ai/DeepSeek-R1", os.getenv("SAMBANOVA_DEEPSEEK_KEY"))
