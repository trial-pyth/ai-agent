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
    original_lorem = _read_text(os.path.join("calculator", "lorem.txt"))
    original_morelorem = _read_text(os.path.join("calculator", "pkg", "morelorem.txt"))

    print(_safe_call(write_file, "calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(_safe_call(write_file, "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(_safe_call(write_file, "calculator", "/tmp/temp.txt", "this should not be allowed"))

    # Best-effort cleanup to avoid impacting other tests.
    try:
        if original_lorem is not None:
            with open(os.path.join("calculator", "lorem.txt"), "w") as f:
                f.write(original_lorem)
    except Exception:
        pass

    try:
        morelorem_path = os.path.join("calculator", "pkg", "morelorem.txt")
        if original_morelorem is None and os.path.isfile(morelorem_path):
            os.remove(morelorem_path)
        elif original_morelorem is not None:
            with open(morelorem_path, "w") as f:
                f.write(original_morelorem)
    except Exception:
        pass


if __name__ == "__main__":
    main()

