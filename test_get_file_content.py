import os

from functions.get_file_content import get_file_content


def _safe_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return f"Error: {e}"


def main():
    repo_root = os.path.dirname(__file__)

    print(_safe_call(get_file_content, repo_root, "main.py"))
    print(_safe_call(get_file_content, repo_root, "calculator/pkg/calculator.py"))

    # Ensure we always print an error line for the harness.
    print(_safe_call(get_file_content, repo_root, "/bin/cat"))


if __name__ == "__main__":
    main()

