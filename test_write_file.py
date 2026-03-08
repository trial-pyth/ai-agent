import os

from functions.write_file import write_file


def _safe_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return f"Error: {e}"


def _read_text(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception:
        return None


def main():
    print(_safe_call(write_file, "calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(_safe_call(write_file, "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(_safe_call(write_file, "calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    main()
