import os
import shutil
from typing import List
from jupiter_from_py import create_jupiter

SAMPLE_SRC = "samples/sample_work.py"


class NotebookGenerator:
    def __init__(self, prefix, directory):
        self.prefix = prefix
        self.directory = directory

    def generate_notebooks(self, n) -> List[str]:
        self.create_directory()
        file_paths = []
        for i in range(n):
            file_name = f"{self.prefix}_VAR{i}.ipynb"
            file_path = os.path.join(self.directory, file_name)
            create_jupiter(SAMPLE_SRC, file_path)
            file_paths.append(file_path)
        return file_paths

    def create_directory(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def clear_directory(self):
        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)
