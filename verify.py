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
You are a helpful Enterprise Architect called Ruth. Ensure the code adheres to the provided patterns and guardrails. Respond in a structured JSON format with fields 'status' and 'description'.

The code does not adhere to the guardrails and standards retuurn pass in the status field otherwise return fail in the status field and populate the descrition field with the reason.

DO NOT RESPOND WITH ```json in the payload

THIS IS AN EXAMPLE FORMAT FOR A FAILED
{
    "status": "fail",
    "description": "The code does not adhere to the following guardrails: \n1. CLM-GUARDRAIL-04: Data Enrichment - The register_customer method does not call `DataEnrichmentService.enrich` before saving the customer data.\n2. GRP-PATTERN-03: Message Translator - Specific message translation mapping based on formats is missing."
}

THIS IS AN EXAMPLE FORMAT FOR A PASS
{
    "status": "pass",
    "description": ""
}
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
