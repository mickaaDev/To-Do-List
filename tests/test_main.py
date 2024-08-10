from fastapi.testclient import TestClient
import random
import string
from app.api.main import app

client = TestClient(app)


def generate_random_string(length=8):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits, k=length
        )
    )


test_tmp_user_id = 0
test_tmp_task_id = 0
test_token = ""


def test_sign_up():
    username = generate_random_string()
    password = generate_random_string()
    global test_tmp_user_id
    response = client.post(
        "/users/",
        json={"username": username, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {
        "username": username,
        "disabled": False,
        "full_name": None,
        "id": response.json().get("id"),
        "tasks": []
    }
    test_tmp_user_id = response.json().get("id")


def test_read_users():
    response = client.get("/users/")

    assert len(response.json()) > 0
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


def test_read_user():
    user_id = 1
    response = client.get(f"/user/{user_id}")

    assert response.status_code == 200
    assert response.json() == {
        "username": "test",
        "disabled": False,
        "full_name": None,
        "id": response.json().get("id"),
        "tasks": []
    }

    response_v2 = client.get(f"/user/{100000}")

    assert response_v2.status_code == 404
    assert response_v2.json().get('detail') == "User not found"


def test_delete_user():
    response = client.delete(
        f"/users/{test_tmp_user_id}",
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted successfully!"}

    response_v2 = client.delete(
        f"/users/{test_tmp_user_id}",
    )
    assert response_v2.status_code == 200
    assert response_v2.json().get("detail") == "User does not exist in DB."
    assert response_v2.json().get("status_code") == 400


def test_create_item_for_user():
    global test_tmp_task_id
    user_id = 4
    response = client.post(
        f"/users/{user_id}/items/",
        json={
            "title": "test-03:24",
            "description": "test",
            "complete": False
        }
    )
    assert response.status_code == 200
    assert response.json() == {
            "id": response.json()['id'],
            "title": response.json()['title'],
            "description": response.json()["description"],
            "created": response.json()['created'],
            "owner_id": user_id
    }
    test_tmp_task_id = response.json().get("id")


def test_read_tasks():
    response = client.get("/tasks/")

    assert len(response.json()) > 0
    assert isinstance(response.json(), list)
    assert response.status_code == 200
    for task in response.json():
        assert isinstance(task, dict)
        assert "id" in task and isinstance(task["id"], int)
        assert "title" in task and isinstance(task["title"], str)
        assert "description" in task and isinstance(task["description"], str)


def test_login_for_access_token():
    response = client.post(
        "/token",
        data={"username": "", "password": ""}
    )

    global test_token

    assert response.status_code == 200
    assert response.json().get("token_type") == "bearer"
    assert isinstance(response.json().get("access_token"), str)
    test_token = response.json().get("access_token")

    response_v2 = client.post(
        "/token",
        data={"username": "error", "password": "error"}
    )

    assert response_v2.status_code == 401
    assert response_v2.json().get("detail") == "Incorrect username or password"


def test_delete_task():
    response = client.delete(
        f"/tasks/{test_tmp_task_id}",
        headers={
            'Authorization': f"Bearer {test_token}"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Task was deleted"}

    response_v2 = client.delete(
        f"/tasks/{0}",
        headers={
            'Authorization': f"Bearer {test_token}"
        }
    )

    assert response_v2.json().get("status_code") == 400
    assert response_v2.json().get("detail") == "Task does not exist in DB."


def test_read_user_me():
    response = client.get(
        "/user/me/",
        headers={
            'Authorization': f"Bearer {test_token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json().get("id"), int)
    assert response.json().get("disabled") == False
    assert isinstance(response.json(), dict)
    assert isinstance(response.json().get("username"), str)
