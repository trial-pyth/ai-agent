from config import MAX_CHARS
import os
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file relative to the working directory, truncating long files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not int the working dir'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'

    file_content_string = ""
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += (
                    f'[...file "{file_path}" truncated at 10000 characters]'
                )
        return file_content_string

    except Exception as e:
        return f"Exception reading file: {e}"
    
