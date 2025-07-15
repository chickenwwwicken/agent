from functions.get_files_info import get_files_info

result_current = """
    Result for current directory:
     - main.py: file_size=576 bytes, is_dir=False
     - tests.py: file_size=1343 bytes, is_dir=False
     - pkg: file_size=92 bytes, is_dir=True
     - lorem.txt: file_size=28 bytes, is_dir=False
    """

result_pkg = """
    Result for 'pkg' directory:
     - calculator.py: file_size=1739 bytes, is_dir=False
     - render.py: file_size=768 bytes, is_dir=False
     - __pycache__: file_size=96 bytes, is_dir=True
     - morelorem.txt: file_size=26 bytes, is_dir=False
    """

result_bin = 'Error: Cannot list "/bin" as it is outside the permitted working directory'

result_outside = 'Error: Cannot list "../" as it is outside the permitted working directory'


def main():

    current_test = get_files_info("calculator", ".")
    pkg_test = get_files_info("calculator", "pkg")

    # current dir test
    if "pkg:" in current_test.split() and "tests.py:" in current_test.split():
        print(get_files_info("calculator", "."))
    else:
        print(get_files_info("calculator", "."))

    # pkg test
    if "render.py:" in pkg_test.split() and "calculator.py:" in pkg_test.split():
        print(get_files_info("calculator", "pkg"))
    else:
        print(get_files_info("calculator", "pkg"))

    # bin test
    if get_files_info("calculator", "/bin") == result_bin: 
        print(get_files_info("calculator", "/bin"))
    else:
        print(get_files_info("calculator", "/bin"))

    # ../ test
    if get_files_info("calculator", "../") == result_outside: 
        print(get_files_info("calculator", "../"))
    else:
        print(get_files_info("calculator", "../"))

if __name__ == "__main__":
    main()


