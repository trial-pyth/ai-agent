import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory, optionally passing arguments, and returns combined stdout/stderr output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        try:
            common = os.path.commonpath([abs_working_dir, abs_file_path])
        except ValueError:
            common = ""

        if common != abs_working_dir:
            return (
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]
        if args:
            command.extend([str(a) for a in args])

        completed = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        parts = []
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        if stdout == "" and stderr == "":
            parts.append("No output produced")
        else:
            if stdout != "":
                parts.append(f"STDOUT:\n{stdout}")
            if stderr != "":
                parts.append(f"STDERR:\n{stderr}")

        return "\n".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"
