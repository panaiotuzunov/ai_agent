import os
from dotenv import load_dotenv
from google import genai
from sys import argv, exit
from google.genai import types
from call_function import available_functions


def main():
    if (len(argv) == 1):
        print("The application needs one argument")
        print("Exiting...")
        exit(1)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    if not response.function_calls:
        print(response.text)
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    if (len(argv) == 3 and argv[2] == "--verbose"):
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

main()

