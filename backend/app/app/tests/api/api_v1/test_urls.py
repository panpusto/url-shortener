from fastapi.testclient import TestClient
from app.core.config import settings


def test_create_url(client: TestClient):
    response = client.post(
        url="/urls",
        json={"target_url": "https://www.python.org/"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["updated_at"] is not None
    assert len(data["key"]) == 5
    assert data["target_url"] == "https://www.python.org/"
    assert data["id"] is not None
    assert data["created_at"] is not None
    assert len(data["secret_key"]) == 14
    assert data["is_active"] is True
    assert data["clicks"] == 0


def test_create_url_invalid_data(client: TestClient):
    response = client.post(
        url="/urls",
        json={"target_url": "Hello"}
    )
    assert response.status_code == 422


def test_read_url(client: TestClient, url_dict: dict):
    key = url_dict.get("key")
    response = client.get(
        url=f"/{key}",
        follow_redirects=False
    )
    assert response.status_code == 307


def test_read_invalid(client: TestClient):
    response = client.get(
        url=f"/fake_key",
        follow_redirects=False
    )
    assert response.status_code == 404
    assert "detail" in response.json()


def test_read_url_info(client: TestClient, url_dict: dict):
    secret_key = url_dict.get("secret_key")
    response = client.get(
        url=f"/admin/{secret_key}"
    )
    data = response.json()
    assert response.status_code == 200
    assert data["target_url"] == url_dict["target_url"]
    assert data["url"] == (settings.base_url + "/" + url_dict["key"])
    assert data["admin_url"] == (settings.base_url + "/admin/" + secret_key)
    assert data["is_active"] == url_dict["is_active"]
    assert data["clicks"] == url_dict["clicks"]


def test_read_url_info_invalid(client: TestClient):
    response = client.get(
        url="/admin/fake_secret_key"
    )
    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_url(client: TestClient, url_dict: dict):
    secret_key = url_dict.get("secret_key")
    response = client.delete(
        url=f"/admin/{secret_key}"
    )
    assert response.status_code == 200
    assert "detail" in response.json()


def test_delete_url_invalid(client: TestClient):
    response = client.delete(
        url="/admin/fake_secret_key"
    )
    assert response.status_code == 404
    assert "detail" in response.json()
