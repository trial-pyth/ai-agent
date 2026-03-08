from functions.run_python_file import run_python_file


def _safe_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return f"Error: {e}"


def main():
    print(_safe_call(run_python_file, "calculator", "main.py"))
    print(_safe_call(run_python_file, "calculator", "main.py", ["3 + 5"]))
    print(_safe_call(run_python_file, "calculator", "tests.py"))
    print(_safe_call(run_python_file, "calculator", "../main.py"))
    print(_safe_call(run_python_file, "calculator", "nonexistent.py"))
    print(_safe_call(run_python_file, "calculator", "lorem.txt"))


if __name__ == "__main__":
    main()

