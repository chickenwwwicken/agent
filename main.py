import sys
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

def main():
    # sys.argv is str after the "run" command.
    user_prompt = sys.argv[1]

    # creating list for conversation
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # error if no prompt
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <'prompt'>")
        sys.exit(1)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
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
