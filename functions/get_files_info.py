import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    else:
        if directory == ".":
            info_list = [f"Result for current directory:"]
        else:
            info_list = [f"Result for '{directory}' directory:"]
        try:
            for file in os.listdir(full_path):
                file_name = file
                file_path = os.path.join(full_path, file)
                file_size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)
                info_list.append(f' - {file_name}: file_size={file_size} bytes, is_dir={is_dir}')
            return "\n".join(info_list)
        except Exception as e:
            info_list.append(f"Error: {e}")
            return "\n".join(info_list)
