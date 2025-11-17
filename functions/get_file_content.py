import os
import config

from google.genai import types

def get_file_content(working_directory, file_path):
    # working_directory absolute path
    work_abs_path = os.path.abspath(working_directory)
    # file_path full path using working_directory's absolute path
    file_full_path = os.path.join(work_abs_path, file_path)

    # if file not in the working directory
    if not file_full_path.startswith(work_abs_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # if file_path leads to something that is not a file
    if not os.path.isfile(file_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # reading the file and ending it if more than 10k chars
        with open(file_full_path) as f:
            content = f.read()
            if len(content) > config.MAX_CHARS:
                truncated_message = content[:config.MAX_CHARS] + f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
                return truncated_message
            return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {config.MAX_CHARS} characters of the content from a specified file within the working directory",
    parameters=types.Schema(
         type=types.Type.OBJECT,
         properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
    ),
)
