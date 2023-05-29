from locust import HttpUser, task, between
import os

FILE_PATH = "server/generation/samples/results/sample.ipynb"


class WebsiteUser(HttpUser):
    wait_time = between(1, 2.5)

    def on_start(self):
        self.file_key = None
        self.state = "upload"

    @task(1)
    def post_file(self):
        with open(FILE_PATH, "rb") as f:
            data = {"file": (os.path.basename(FILE_PATH), f)}
            response = self.client.post("file/test/upload", files=data)
            if response.status_code == 200:
                self.file_key = response.text

    @task(2)
    def get_file(self):
        if self.file_key:
            self.client.get(
                f"file/test/get?file_key={self.file_key}&file_name=test_file"
            )
