import os
import shutil


class NotebookGenerator:
    def __init__(self, prefix, directory):
        self.prefix = prefix
        self.directory = directory

    def generate_notebooks(self, n):
        self.create_directory()
        self.clear_directory()

    def create_directory(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def clear_directory(self):
        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)
