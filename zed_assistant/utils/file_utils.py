import os


def read_file_contents(folder_path: str, file_name: str) -> str:
    folder = os.path.dirname(folder_path)
    path = os.path.join(folder, file_name)
    with open(path, "r") as file:
        return file.read()
