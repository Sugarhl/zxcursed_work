class FileStorage:
    def save_file(self, content):
        raise NotImplementedError("save_file method must be implemented by the subclass")

    def get_file(self, file_id):
        raise NotImplementedError("get_file method must be implemented by the subclass")

    def delete_file(self, file_id):
        raise NotImplementedError("delete_file method must be implemented by the subclass")
