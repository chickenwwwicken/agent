import os
import sys
import subprocess

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
    run_exec_list = ["uv", "run", file_full_path]
    for arg in args:
        run_exec_list.append(f'{arg}')

    # subprocess.run object that returns:
    # a completed.process object
    run_this_b = subprocess.run(
        run_exec_list,
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
            output_list = [f'STDOUT: {str(stdout)}', f'STDERR: {str(stderr)}']
            return "\n".join(output_list)

    except Exception as e:
            return f"Error: {e}"




