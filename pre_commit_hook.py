#!/usr/bin/env python

import subprocess
import asyncio
import os
import json
from verify import main as verify_with_openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_flake8():
    print("Running flake8...")
    result = subprocess.run(
        ['flake8', '--config', '.flake8'], capture_output=True, text=True
    )
    if result.returncode != 0:
        print("flake8 failed with output:\n", result.stdout)
        return False
    print("flake8 passed")
    return True

async def validate_with_openai():
    print("Starting OpenAI validation...")
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
        f"Code to be validated:\n{code}\n\n"
        """
        You must analyse the 'Code to be validated' adheres to the guardrails and standards return "pass" in the status field. You must check the code
        
        If the code does not adhere to the guardrails and standards return "fail" in the status field and populate the description field with the reason. If failed you must provide the pattern referecne number(s), guardail referecne number(s) or standard(s) referecne number

        DO NOT RESPOND WITH ```json in the payload

        YOU MUST ONLY USE THIS FORMAT
        {
            "status": "",
            "description": ""
        }
        """
    )

    print(f"Prompt sent to OpenAI:\n{prompt}")

    # Send the prompt to OpenAI and get the response
    response = await verify_with_openai(prompt)
    print("OpenAI Validation Response:", response)

    # Clean the response to remove any non-JSON text and parse it
    response = response.strip().strip('```json').strip('```').replace('\n', ' ')

    # Parse the JSON response
    try:
        response_json = json.loads(response)
        status = response_json.get("status", "").lower()
        description = response_json.get("description", "")
        print(f"Status: {status}, Description: {description}")
        if status == "pass":
            print("OpenAI validation passed")
            return True
        else:
            print(f"Pre-commit checks failed based on OpenAI validation: {description}")
            return False
    except json.JSONDecodeError as e:
        print(f"Failed to decode OpenAI response: {e}")
        print("Pre-commit checks failed due to invalid response format.")
        return False

if __name__ == "__main__":
    print("Pre-commit hook started")
    if not run_flake8():
        print("Pre-commit checks failed due to flake8.")
        exit(1)

    # Check if OPENAI_CHECK environment variable is set to "true"
    openai_check = os.getenv("OPENAI_CHECK", "true").lower()
    openai_check = True
    print(f"OPENAI_CHECK is set to {openai_check}")
    if openai_check == "true":
        # Run OpenAI validation
        validation_result = asyncio.run(validate_with_openai())
        if not validation_result:
            exit(1)
    print("Pre-commit hook completed successfully")
