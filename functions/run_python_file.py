import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a Python file (.py) within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file (.py) to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional arguments to pass to the Python file",
                },
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        text = ""
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            text += f'    Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            return text.strip()
        if not os.path.isfile(target_dir):
            text += f'    Error: "{file_path}" does not exist or is not a regular file'
            return text.strip()

        if not file_path.endswith(".py"):
            text += f'    Error: "{file_path}" is not a Python file'
            return text.strip()

        command = ["python", target_dir]
        if args:
            command.extend(args)

        result = subprocess.run(command,cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            text += f'Process exited with code {result.returncode}'
        if not result.stdout and not result.stderr:
            text += f"No output produced"
        if result.stdout:
            text += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            text += f"STDERR:\n{result.stderr}"

        return text.strip()

    except Exception as e:
        text += f"Error: executing Python file: {e}"
        return text.strip()