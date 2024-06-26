import os
import openai
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the API key is set in the environment
openai.api_key = os.getenv("OPENAI_API_KEY")
print(f"Using OpenAI API key: {openai.api_key}")

system_prompt = """
You are a helpful Enterprise Architect called Ruth.
"""

async def async_openai_call(prompt):
    print("Calling OpenAI API...")
    client = AsyncOpenAI()
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

async def main(prompt):
    response = await async_openai_call(prompt)
    return response

# This part is for testing the function independently
if __name__ == "__main__":
    user_input = "Your prompt here"
    result = asyncio.run(main(user_input))
    print(result)
