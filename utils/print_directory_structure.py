# utils/print_directory_structure.py

import os

def print_directory_structure(start_path, indent='', skip_folders=None, skip_contents=None):
    if skip_folders is None:
        skip_folders = {'.git', '__pycache__', '.pytest_cache'}
    if skip_contents is None:
        skip_contents = {'streamdata'}

    for item in sorted(os.listdir(start_path)):
        item_path = os.path.join(start_path, item)
        if os.path.isdir(item_path):
            if item in skip_folders:
                continue
            print(f"{indent}📁 {item}")
            if item not in skip_contents:
                print_directory_structure(item_path, indent + '    ', skip_folders, skip_contents)
        else:
            # Check if any part of the path is in skip_folders or if parent is in skip_contents
            parts = os.path.relpath(item_path, start_path).split(os.sep)
            if not any(p in skip_folders for p in parts):
                print(f"{indent}📄 {item}")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print("Project Directory Structure:\n")
    print_directory_structure(project_root)
