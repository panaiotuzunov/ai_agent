import os
from dotenv import load_dotenv
from google import genai
from sys import argv, exit
from google.genai import types


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
    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt))
    print(response.text)
    if (len(argv) == 3 and argv[2] == "--verbose"):
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

main()

