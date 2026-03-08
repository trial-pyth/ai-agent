import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
""".strip()
    if len(sys.argv) < 2:
        print("I need a prompt!")
        sys.exit(2)
    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        print(sys.argv[2])
        verbose_flag = True
    prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    function_calls = getattr(response, "function_calls", None)
    if function_calls:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)
    if response is None or response.usage_metadata is None:
        print("Response is malformed")
        return
    if verbose_flag:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.prompt_token_count}")

if __name__ == "__main__":
    main()
