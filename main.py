import os
from dotenv import load_dotenv
from google import genai
from sys import argv, exit
from google.genai import types
from call_function import available_functions, call_function


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
    system_prompt = system_prompt = """
You are a helpful AI agent designed to help the user write code within their codebase.

When a user asks a question or makes a request, make a function call plan. For example, if the user asks "what is in the config file in my current directory?", your plan might be:

1. Call a function to list the contents of the working directory.
2. Locate a file that looks like a config file
3. Call a function to read the contents of the config file.
4. Respond with a message containing the contents

You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security.

You are called in a loop, so you'll be able to execute more and more function calls with each message, so just take the next step in your overall plan.

Most of your plans should start by scanning the working directory (`.`) for relevant files and directories. Don't ask me where the code is, go look for it with your list tool.

Execute code (both the tests and the application itself, the tests alone aren't enough) when you're done making modifications to ensure that everything works as expected.
"""
    is_verbose = (len(argv) == 3 and argv[2] == "--verbose")
    
    for i in range(20):
        try:
            response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
            
            for candidate in response.candidates:
                messages.append(candidate.content)
            
            if not response.function_calls:
                print("Final response:")
                print(response.text)
                break
            
            if response.function_calls:
                for function_call_part in response.function_calls:
                    result = call_function(function_call_part, is_verbose)
                    if not result.parts[0].function_response.response:
                        raise Exception("FATAL. No function response found.")
                    if is_verbose:
                        print(f"-> {result.parts[0].function_response.response}")
                    messages.append(result)

            if is_verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        except Exception as e:
            print(f"Error: {str(e)}")
            break
    
main()

