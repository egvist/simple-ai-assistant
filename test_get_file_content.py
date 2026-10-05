from functions.get_files_content import get_file_content



ext = ["main.py","pkg/calculator.py","/bin/cat","/pkg/does_not_exist.py"]

for i in ext:
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    result = get_file_content("calculator", i)
    print(result)
    print(f"lorem.txt truncated: {'truncated' in result}")
