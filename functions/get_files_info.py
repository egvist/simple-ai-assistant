import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        text = ""
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if target_dir == working_dir_abs:
            text += f"Result for current directory:\n"
        else:
            text += f"Result for '{directory}' directory:\n"

        if not valid_target_dir:
            text += f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
            return text.strip()
        if not os.path.isdir(target_dir):
            text += f'    Error: "{directory}" is not a directory'
            return text.strip()

        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            isdir = os.path.isdir(item_path)
            size = os.path.getsize(item_path)
            text += f"  - {item}: file_size={size} bytes, is_dir={isdir}\n"

        return text.strip()



    except Exception as e:
        text += f"Error: {str(e)}"
        return text.strip()