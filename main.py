import sys
import os
from google import genai
from config import MAX_ITERS
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions, call_function

# ------------------------------------------------------------------------

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []

    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    # error if no prompt
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator"')
        sys.exit(1)


    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # sys.argv is str after the "run" command.
    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    # creating list for conversation
    messages = [
        types.Content(
            role="user", 
            parts=[
                types.Part(
                    text=user_prompt
                )
            ]
        ),
    ]

    # agentic while loop --------------------------------------------------------
    # agentic while loop --------------------------------------------------------
    # agentic while loop --------------------------------------------------------

    iteration_count = 0

    while iteration_count < MAX_ITERS: # max iterations is 20
        iteration_count += 1

        final_text = generate_content(client, messages, verbose)

        if final_text:
            print(final_text)
            break




# ------------------------generate content func----------------------------------
# ------------------------generate content func----------------------------------
# ------------------------generate content func----------------------------------

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        # giving the messages list to the model so it has context
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:

        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # no verbose flag
    if not response.function_calls:
        return response.text, []


    response_list = []

    for function_call_part in response.function_calls:

        function_call_result = call_function(function_call_part, verbose=verbose)

        # raise exception if function call returns empty
        if not function_call_result.parts[0].function_response.response:
            raise Exception("fatal error 444")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        if function_call_result.parts[0].function_response.response:
            response_list.append(function_call_result.parts[0])


    return response.text, response_list


if __name__ == "__main__":
    main()
