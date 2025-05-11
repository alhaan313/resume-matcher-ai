import os
from cerebras.cloud.sdk import Cerebras

from dotenv import load_dotenv

load_dotenv()
# Set up the Cerebras client
client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")  # Make sure the API key is set in your environment
)

# Create a simple test function to interact with the API
def test_cerebras_api():
    # Define the test prompt for resume generation
    test_prompt = [
        {
            "role": "system",
            "content": "You are an assistant for generating LaTeX-based resumes."
        },
        {
            "role": "user",
            "content": "Write me a resume generator based on job description using LaTeX code."
        }
    ]

    # Make the API call to generate the response
    stream = client.chat.completions.create(
        messages=test_prompt,
        model="llama3.1-8b",  # Use the model you need (adjust as per your actual model)
        stream=True,
        max_completion_tokens=2048,
        temperature=0.5,  # Adjust temperature if you want more or less randomness
        top_p=1
    )

    # Process and print the response stream
    print("Generating LaTeX resume:")
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")

# Call the function to test the API
if __name__ == "__main__":
    test_cerebras_api()
