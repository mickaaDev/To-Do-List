import random
import string
import pytest
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


class TestUserManagement:

    @pytest.fixture
    def create_user(self):

        username = generate_random_string()
        password = generate_random_string()

        response = client.post(
            "/users/",
            json={"username": username, "password": password}
        )

        assert response.status_code == 200
        user_id = response.json().get("id")

        yield {
            "username": username,
            "password": password,
            "id": user_id
        }

        client.delete(f"/users/{user_id}")

    @pytest.fixture
    def get_token(self, create_user):

        response = client.post(
            "/token",
            data={
                "username": create_user["username"],
                "password": create_user["password"]
            }
        )

        assert response.status_code == 200
        token = response.json().get("access_token")
        return f"Bearer {token}"

    def test_sign_up(self, create_user):

        assert create_user["id"] >= 0

    def test_create_task_for_user(self, get_token, create_user):
        user_id = create_user["id"]
        response = client.post(
            "/users/task/",
            json={
                "title": "test-03:24",
                "description": "test",
                "complete": False,
                "owner_id": user_id
            },
            headers={
                'Authorization': get_token
            }
        )

        task_id = response.json().get('id')
        assert response.status_code == 200
        assert isinstance(task_id, int)
        assert 'id' in response.json()

        client.delete(
            f"/tasks/{task_id}",
            headers={
                'Authorization': get_token
            }
        )

    def test_delete_task(self, get_token, create_user):

        user_id = create_user["id"]
        response = client.post(
            "/users/task/",
            json={
                "title": "test-03:24",
                "description": "test",
                "complete": False,
                "owner_id": user_id
            },
            headers={
                'Authorization': get_token
            }
        )
        assert response.status_code == 200
        task_id = response.json().get('id')

        response_v2 = client.delete(
            f"/tasks/{task_id}",
            headers={
                'Authorization': get_token
            }
        )
        assert response_v2.json() == {"detail": "Task was deleted"}
        response_v3 = client.delete(
            f"/tasks/{-1}",
            headers={
                'Authorization': get_token
            }
        )

        assert response_v3.json().get("status_code") == 400
        assert response_v3.json().get("detail") == "Task does not exist in DB."

    def test_updates_task(self, create_user, get_token):

        user_id = create_user["id"]

        response = client.post(
            "/users/task/",
            json={
                "title": "test-03:24",
                "description": "test",
                "complete": False,
                "owner_id": user_id
            },
            headers={
                'Authorization': get_token
            }
        )
        task_id = response.json().get('id')
        response_v2 = client.patch(
            f"/task/{task_id}",
            json={
                "title": "test-03:24",
                "description": "test",
                "complete": False,
                "owner_id": user_id
            },
            headers={
                'Authorization': get_token
            }
        )
        assert response_v2.status_code == 200
        assert response_v2.json().get("title") == "test-03:24"
        assert response_v2.json().get("description") == "test"
        assert response_v2.json().get("owner_id") == user_id

        client.delete(
            f"/tasks/{task_id}",
            headers={
                'Authorization': get_token
            }
        )

    def test_delete_user(self, create_user, get_token):

        response = client.delete(f"/users/{create_user['id']}")
        assert response.status_code == 200
        assert response.json() == {"detail": "User deleted successfully!"}


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
