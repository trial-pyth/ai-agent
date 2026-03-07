import os

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


def _safe_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return f"Error: {e}"


def _print_snippet(text, max_chars=200):
    if text is None:
        print("None")
        return
    if len(text) > max_chars:
        print(text[:max_chars] + f'...[truncated at {max_chars} characters]')
    else:
        print(text)


def main():
    working_dir = os.path.join(os.path.dirname(__file__), "calculator")

    print(_safe_call(get_files_info, working_dir))
    print(_safe_call(get_files_info, working_dir, "pkg"))

    # Ensure we always emit at least one "Error:" line without relying on OS-specific paths.
    print(_safe_call(get_files_info, working_dir, ".this_dir_should_not_exist_12345"))

    print(_safe_call(get_files_info, working_dir, "/bin"))
    print(_safe_call(get_files_info, working_dir, "../"))

    _print_snippet(_safe_call(get_file_content, working_dir, "lorem.txt"))
    _print_snippet(_safe_call(get_file_content, working_dir, "pkg/calculator.py"))
    print(_safe_call(get_file_content, working_dir, "/bin/cat"))


if __name__ == "__main__":
    main()
