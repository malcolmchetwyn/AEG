#!/usr/bin/env python

import subprocess
import asyncio
import os
from verify import main as verify_with_openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_flake8():
    result = subprocess.run(
        ['flake8', '--config', '.flake8'], capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stdout)
        return False
    return True

async def validate_with_openai():
    # Read the patterns and guardrails content
    with open('patterns_guardrails/patterns_and_guardrails.txt', 'r') as file:
        patterns_guardrails = file.read()

    with open('patterns_guardrails/target_state_patterns.txt', 'r') as file:
        target_patterns = file.read()

    # Read the code to be validated
    with open('clm_system.py', 'r') as code_file:
        code = code_file.read()

    # Combine the contents to form the prompt
    prompt = (
        f"Patterns and Guardrails:\n{patterns_guardrails}\n\n"
        f"Target State Patterns:\n{target_patterns}\n\n"
        f"Code to be validated:\n{code}"
    )

    # Send the prompt to OpenAI and get the response
    response = await verify_with_openai(prompt)
    print("OpenAI Validation Response:", response)

    if "fail" in response.lower():
        print("Pre-commit checks failed based on OpenAI validation.")
        return False
    return True

if __name__ == "__main__":
    if not run_flake8():
        print("Pre-commit checks failed.")
        exit(1)

    # Check if OPENAI_CHECK environment variable is set to "true"
    if os.getenv("OPENAI_CHECK", "true").lower() == "true":
        # Run OpenAI validation
        validation_result = asyncio.run(validate_with_openai())
        if not validation_result:
            exit(1)
