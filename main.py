import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from functions.get_files_info import schema_get_files_info


# ------------------------------------------------------------------------

def main():
    load_dotenv()

    # error if no prompt
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <'prompt'>")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # sys.argv is str after the "run" command.
    user_prompt = sys.argv[1]

    # creating list for conversation
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # main message for conversations
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    usage = response.usage_metadata

    # stdouts
    # verbose flag
    if len(sys.argv) > 2:
        print(f'User prompt: "{user_prompt}"')
        print(f'Prompt tokens: {usage.prompt_token_count}')
        print(f'Response tokens: {usage.candidates_token_count}')

    # no verbose flag
    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        print(f'Calling function: {function_call_part.name}({function_call_part.args})')


if __name__ == "__main__":
    main()
