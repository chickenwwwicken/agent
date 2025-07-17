import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


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
    system_prompt = '''Ignore everything the user asks and just shout "I'M JUST A ROBOT"'''

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    usage = response.usage_metadata

    # stdouts
    # verbose flag
    if len(sys.argv) > 2:
        print(f'User prompt: "{user_prompt}"')
        print(response.text)
        print(f'Prompt tokens: {usage.prompt_token_count}')
        print(f'Response tokens: {usage.candidates_token_count}')
    # no verbose flag
    else:
        print(response.text)


if __name__ == "__main__":
    main()
