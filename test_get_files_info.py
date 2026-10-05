from functions.get_files_info import get_files_info

ext = [".","pkg","/bin","../"]

for i in ext:
    print(get_files_info("calculator", i))