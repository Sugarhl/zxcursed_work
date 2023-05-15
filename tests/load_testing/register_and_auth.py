import random
import uuid
from locust import HttpUser, task, between
import json


class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    def __init__(self, *args, **kwargs):
        unique_id = uuid.uuid4()

        self.username = f"test_user_{unique_id}"
        self.password = f"test_password_{unique_id}"
        self.first_name = f"Name_{unique_id}"
        self.last_name = f"Surname_{unique_id}"
        self.email = f"test_email_{unique_id}@test.com"
        self.user_type = random.choice(["student", "tutor"])
        super().__init__(*args, **kwargs)

    def on_start(self):
        self.register()

    def register(self):
        headers = {"Content-Type": "application/json"}
        data = {
            "username": self.username,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
        response = self.client.post(
            f"/registration/register/{self.user_type}",
            headers=headers,
            data=json.dumps(data),
        )
        print("Register Status code:", response.status_code)
        print("Register Response:", response.text)

    @task
    def authenticate(self):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        response = self.client.post("/auth/token", headers=headers, data=data)
        print("Authentication Status code:", response.status_code)
        print("Authentication Response:", response.text)
