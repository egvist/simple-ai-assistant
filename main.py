import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from call_function import available_functions, call_function
from prompt import system_prompt
import json


def generate_content(client, messages):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    return response


def main():
    load_dotenv()

    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set in the environment variables."
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    prompt = args.user_prompt
    verbose = args.verbose

    
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    for _ in range(20):
        response = generate_content(client, messages)

        if response.usage is None:
            raise RuntimeError(
                "Response usage is None. Please check the API response."
            )

        prompt_tokens = response.usage.prompt_tokens
        response_tokens = response.usage.completion_tokens

        if verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        message = response.choices[0].message
        messages.append(message)
    
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=verbose,)
                if not result_message["content"]:
                    raise RuntimeError("Function call returned empty content.")
                messages.append(result_message)
                if verbose:
                    print(f"-> {result_message['content']}")

        else:
            print(f"Response: {message.content}")
            return
    print("Error: Maximum iterations reached")
    sys.exit(1)

if __name__ == "__main__":
    main()