import pytest

from src.models import Spot


@pytest.fixture
def test_spot(db, test_user):
    spot = Spot(
        title="Test Cafe",
        description="A cozy cafe",
        category="cafe",
        rating=4.5,
        latitude=59.3293,
        longitude=18.0686,
        address="Stockholm, Sweden",
        best="Cappuccino",
        best_time="Morning",
        price_level=2,
        user_id=test_user.id,
    )
    db.add(spot)
    db.commit()
    db.refresh(spot)
    return spot


def test_create_spot(client, auth_headers):
    response = client.post(
        "/api/spots",
        headers=auth_headers,
        json={
            "title": "New Spot",
            "description": "A great place",
            "category": "restaurant",
            "rating": 4.0,
            "latitude": 59.3293,
            "longitude": 18.0686,
            "best": "Pizza",
            "price_level": 3,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Spot"
    assert data["category"] == "restaurant"
    assert data["rating"] == 4.0


def test_create_spot_unauthorized(client):
    response = client.post(
        "/api/spots",
        json={
            "title": "New Spot",
            "category": "restaurant",
            "latitude": 59.3293,
            "longitude": 18.0686,
        },
    )
    assert response.status_code == 403


def test_list_spots(client, test_spot):
    response = client.get("/api/spots")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Test Cafe"


def test_list_spots_filter_category(client, db, test_user, test_spot):
    spot2 = Spot(
        title="Test Restaurant",
        category="restaurant",
        latitude=59.3293,
        longitude=18.0686,
        user_id=test_user.id,
    )
    db.add(spot2)
    db.commit()

    response = client.get("/api/spots?category=cafe")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["category"] == "cafe"


def test_list_spots_filter_rating(client, db, test_user, test_spot):
    spot2 = Spot(
        title="Low Rating",
        category="cafe",
        rating=2.0,
        latitude=59.3293,
        longitude=18.0686,
        user_id=test_user.id,
    )
    db.add(spot2)
    db.commit()

    response = client.get("/api/spots?min_rating=4.0")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["rating"] >= 4.0


def test_get_spot(client, test_spot):
    response = client.get(f"/api/spots/{test_spot.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Cafe"
    assert data["id"] == test_spot.id


def test_get_spot_not_found(client):
    response = client.get("/api/spots/99999")
    assert response.status_code == 404


def test_update_spot(client, auth_headers, test_spot):
    response = client.patch(
        f"/api/spots/{test_spot.id}",
        headers=auth_headers,
        json={"title": "Updated Cafe", "rating": 5.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Cafe"
    assert data["rating"] == 5.0


def test_update_spot_unauthorized(client, test_spot):
    response = client.patch(
        f"/api/spots/{test_spot.id}",
        json={"title": "Updated Cafe"},
    )
    assert response.status_code == 403


def test_delete_spot(client, auth_headers, test_spot):
    response = client.delete(f"/api/spots/{test_spot.id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/api/spots/{test_spot.id}")
    assert response.status_code == 404


def test_delete_spot_unauthorized(client, test_spot):
    response = client.delete(f"/api/spots/{test_spot.id}")
    assert response.status_code == 403
