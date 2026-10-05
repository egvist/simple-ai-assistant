import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        text = ""
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            text += f'    Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            return text.strip()
        if os.path.isdir(target_dir):
            text += f'    Error: Cannot write to "{file_path}" as it is a directory'
            return text.strip()

        parent_dir = os.path.dirname(target_dir)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)
            text += f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            return text.strip()

    except Exception as e:
        text += f"Error: {str(e)}"
        return text.strip()