import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file relative to the working directory, creating parent directories if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'
    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"Could not create parent dirs: {parent_dir} = {e}"
    # if not os.path.isfile(abs_file_path):
    #     parent_dir = os.path.dirname(abs_file_path)
    #     try:
    #         os.makedirs(parent_dir)
    #     except Exception as e:
    #         return f"Could not create parent dirs: {parent_dir} = {e}"
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        count = len(content)
        plural = "s" if count != 1 else ""
        return f'Successfully wrote to "{file_path}" {count} character{plural} written'
    except Exception as e:
        return f"Failed to write to file: {file_path}, {e}"
