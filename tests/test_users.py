def test_get_current_user(client, auth_headers, test_user):
    response = client.get("/api/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username


def test_get_current_user_unauthorized(client):
    response = client.get("/api/users/me")
    assert response.status_code == 403


def test_update_current_user(client, auth_headers):
    response = client.patch(
        "/api/users/me",
        headers=auth_headers,
        json={"username": "updateduser"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"


def test_update_current_user_avatar(client, auth_headers):
    response = client.patch(
        "/api/users/me",
        headers=auth_headers,
        json={"avatar_url": "https://example.com/avatar.jpg"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["avatar_url"] == "https://example.com/avatar.jpg"
