import os
import random
import string
import pytest
import asyncio
from fastapi.testclient import TestClient
from app.api.main import app
from dotenv import load_dotenv


load_dotenv()


client = TestClient(app)


def generate_random_string(length=8):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits, k=length
        )
    )


username_v1 = os.getenv('test_user_username')
password_v1 = os.getenv('test_user_password')


class TestUserManagement:

    test_tmp_user_id = 0
    test_tmp_task_id = 0
    test_token = ""
    username = ""
    password = ""

    @classmethod
    def setup_class(self):
        if not self.username:
            self.username = generate_random_string()
        if not self.password:
            self.password = generate_random_string()

    def test_sign_up(self):

        response = client.post(
            "/users/",
            json={"username": self.username, "password": self.password}
        )
        assert response.status_code == 200
        assert response.json() == {
            "username": self.username,
            "disabled": False,
            "full_name": None,
            "id": response.json().get("id"),
            "tasks": []
        }
        self.__class__.test_tmp_user_id = response.json().get("id")

    def test_read_users(self):
        response = client.get("/users/")

        assert len(response.json()) >= 0
        assert isinstance(response.json(), list)
        assert response.status_code == 200
        for user in response.json():
            assert isinstance(user, dict)
            assert "id" in user and isinstance(user["id"], int)
            assert "username" in user and isinstance(user["username"], str)
            assert "full_name" in user and (
                user["full_name"] is None or isinstance(user["full_name"], str)
            )
            assert "disabled" in user and isinstance(user["disabled"], bool)

    def test_read_user(self):
        response = client.get(f"/user/{self.__class__.test_tmp_user_id}")

        assert response.status_code == 200
        assert response.json() == {
            "username": self.__class__.username,
            "disabled": False,
            "full_name": None,
            "id": response.json().get("id"),
            "tasks": []
        }

        response_v2 = client.get(f"/user/{100000}")

        assert response_v2.status_code == 404
        assert response_v2.json().get('detail') == "User not found"

    def test_login_for_access_token(self):
        response = client.post(
            "/token",
            data={
                "username": self.__class__.username,
                "password": self.__class__.password
            }
        )

        assert response.status_code == 200
        assert response.json().get("token_type") == "bearer"
        assert isinstance(response.json().get("access_token"), str)
        self.__class__.test_token = response.json().get("access_token")

        response_v2 = client.post(
            "/token",
            data={"username": "errr", "password": "errr"}
        )

        assert response_v2.status_code == 401
        assert response_v2.json().get(
            "detail"
        ) == "Incorrect username or password"

    def test_create_task_for_user(self):

        response = client.post(
            "/users/task/",
            json={
                "title": "test-03:24",
                "description": "test",
                "complete": False
            },
            headers={
                'Authorization': f"Bearer {self.__class__.test_token}"
            }
        )
        assert response.status_code == 200
        assert response.json() == {
                "id": response.json()['id'],
                "title": response.json()['title'],
                "description": response.json()["description"],
                "created": response.json()['created'],
                "owner_id": self.__class__.test_tmp_user_id
        }
        self.__class__.test_tmp_user_id = response.json().get("id")

    def test_read_user_me(self):
        response = client.get(
            "/user/me/",
            headers={
                'Authorization': f"Bearer {self.__class__.test_token}"
            }
        )

        assert response.status_code == 200
        assert isinstance(response.json().get("id"), int)
        assert response.json().get("disabled") == False
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get("username"), str)

    def test_update_task(self):
        response = client.patch(
            f"/task/{self.__class__.test_tmp_user_id}",
            json={
                "title": "Updated Title",
                "description": "Updated description",
                "complete": True
            },
            headers={
                'Authorization': f"Bearer {self.__class__.test_token}"
            }
        )
        assert response.status_code == 200
        assert response.json().get("id") == self.__class__.test_tmp_user_id
        assert response.json().get("title") == "Updated Title"
        assert response.json().get("description") == "Updated description"

        tmp_task_id = response.json().get("id")

        update_response = client.patch(
            f"/task/{tmp_task_id}",
            json={
                "title": "Another Test Update Title",
                "description": "Another Test Update Update description",
                "complete": False
            },
            headers={
                'Authorization': f"Bearer {self.__class__.test_token}"
            }
        )

        assert update_response.status_code == 200
        assert update_response.json().get(
            "title"
        ) == "Another Test Update Title"
        assert update_response.json().get(
            "description"
        ) == "Another Test Update Update description"

        response_v2 = client.patch(
            f"/task/{10000000}",
            json={
                "title": "Updated Title",
                "description": "Updated description",
                "complete": True
            },

            headers={
                'Authorization': f"Bearer {self.__class__.test_token}"
                    }
        )
        assert response_v2.status_code == 404
        assert response_v2.json() == {
            'detail': 'This task does not belongs to the current user'
        }

    def test_delete_task(self):
        response = client.delete(
            f"/tasks/{self.__class__.test_tmp_user_id}",
            headers={
                'Authorization': f"Bearer {self.__class__.test_token}"
            }
        )
        assert response.status_code == 200
        assert response.json() == {"detail": "Task was deleted"}

        response_v2 = client.delete(
            f"/tasks/{0}",
            headers={
                'Authorization': f"Bearer {self.__class__.test_token}"
            }
        )

        assert response_v2.json().get("status_code") == 400
        assert response_v2.json().get("detail") == "Task does not exist in DB."
    
    def test_delete_user(self):
        response = client.delete(
            f"/users/{self.__class__.test_tmp_user_id}",
        )
        assert response.status_code == 200
        assert response.json() == {"detail": "User deleted successfully!"}

        response_v2 = client.delete(
            f"/users/{self.__class__.test_tmp_user_id}",
        )
        assert response_v2.status_code == 200
        assert response_v2.json().get("detail") == "User does not exist in DB."
        assert response_v2.json().get("status_code") == 400
    test_tmp_user_id = 0
    test_tmp_task_id = 0

class TestItemManagement:
    def test_read_tasks(self):
        response = client.get("/tasks/")

        assert len(response.json()) >= 0
        assert isinstance(response.json(), list)
        assert response.status_code == 200
        for task in response.json():
            assert isinstance(task, dict)
            assert "id" in task and isinstance(task["id"], int)
            assert "title" in task and isinstance(task["title"], str)
            assert "description" in task and isinstance(
                task["description"],
                str
            )
