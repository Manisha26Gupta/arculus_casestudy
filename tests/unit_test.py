import pytest
from app import app, db


@pytest.fixture
def client():
    # Setup: use an in-memory SQLite DB for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_health_ok(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_get_orders_initially_empty(client):
    res = client.get("/orders")
    assert res.status_code == 200
    assert res.get_json() == []


def test_create_order(client):
    res = client.post("/orders", json={"amount": 42.5})
    assert res.status_code == 201
    data = res.get_json()
    assert "id" in data
    assert data["amount"] == 42.5

    # Verify with GET
    res2 = client.get("/orders")
    orders = res2.get_json()
    assert len(orders) == 1
    assert orders[0]["amount"] == 42.5


def test_create_order_invalid_amount(client):
    # Non-numeric
    res = client.post("/orders", json={"amount": "abc"})
    assert res.status_code == 400

    # Negative value
    res = client.post("/orders", json={"amount": -10})
    assert res.status_code == 400


def test_delete_order(client):
    # Create order
    res = client.post("/orders", json={"amount": 15})
    order_id = res.get_json()["id"]

    # Delete
    res2 = client.delete(f"/orders/{order_id}")
    assert res2.status_code == 200
    assert f"Order {order_id} deleted" in res2.get_json()["message"]

    # Verify gone
    res3 = client.get("/orders")
    assert res3.get_json() == []


def test_delete_order_not_found(client):
    res = client.delete("/orders/999")
    assert res.status_code == 404
