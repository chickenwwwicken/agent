import os

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


