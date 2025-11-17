import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    # working_directory absolute path
    work_abs_path = os.path.abspath(working_directory)
    # file_path full path using working_directory's absolute path
    file_full_path = os.path.abspath(os.path.join(work_abs_path, file_path))

    dir_path = os.path.dirname(file_full_path)

    # if file outside working dir, no work
    if os.path.commonpath([work_abs_path, file_full_path]) != work_abs_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_full_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    # same as uv run <path> <flags> 
    commands = ["uv", "run", file_full_path]
    for arg in args:
        commands.append(f'{arg}')

    # subprocess.run object that returns:
    # a completed.process object
    run_this_b = subprocess.run(
        commands,
        capture_output=True,
        timeout=30,
        cwd=dir_path,
        text=True
    )

    try:
        exit_code = run_this_b.returncode
        stdout = run_this_b.stdout
        stderr = run_this_b.stderr

        if exit_code != 0:
            return f"Process exited with code {exit_code}"

        if not stdout and not stderr:
            return 'No output produced.'

        else:
            output_list = [f'STDOUT:\n{str(stdout)}', f'STDERR:\n{str(stderr)}']
            return "\n".join(output_list)

    except Exception as e:
            return f"Error: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)


