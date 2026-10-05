import os
from functions.config import MAX_CHARS

schema_get_files_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Retrieves the content of a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory",
                },
            },
        },
    },
}



def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        text = ""
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            text += f'    Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            return text.strip()
        if not os.path.isfile(target_dir):
            text += f'    Error: File not found or is not a regular file: "{file_path}"'
            return text.strip()

        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        text += f"Error: {str(e)}"
        return text.strip()