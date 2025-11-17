import os

from google.genai import types

def write_file(working_directory, file_path, content):
    # working_directory absolute path
    work_abs_path = os.path.abspath(working_directory)
    # file_path full path using working_directory's absolute path
    file_full_path = os.path.join(work_abs_path, file_path)

    # if file not in the working directory
    # new os.path function
    # compares path components, not just strings.
    if os.path.commonpath([work_abs_path, file_full_path]) != work_abs_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    dir_path = os.path.dirname(file_full_path)

    try:
        os.makedirs(dir_path, exist_ok=True)
        with open(file_full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file"
            ),
        },
        required=["file_path", "content"],
    ),
)


