import pytest
from app import app, db, Order


@pytest.fixture
def client():

    # Use in-memory SQLite DB for integration tests
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_db_connection(client):
    """Verify database is reachable and usable"""
    with app.app_context():
        # Direct DB insert
        o = Order(amount=123.45)
        db.session.add(o)
        db.session.commit()

        found = Order.query.first()
        assert found is not None
        assert found.amount == 123.45


def test_orders_api_flow(client):
    """Verify /orders works end-to-end"""
    # Initially empty
    res = client.get("/orders")
    assert res.status_code == 200
    assert res.get_json() == []

    # Create order
    res2 = client.post("/orders", json={"amount": 55.5})
    assert res2.status_code == 201
    created = res2.get_json()
    assert "id" in created
    assert created["amount"] == 55.5

    # List should now contain the new order
    res3 = client.get("/orders")
    data = res3.get_json()
    assert len(data) == 1
    assert data[0]["amount"] == 55.5

    # Delete the order
    order_id = data[0]["id"]
    res4 = client.delete(f"/orders/{order_id}")
    assert res4.status_code == 200
    assert f"Order {order_id} deleted" in res4.get_json()["message"]

    # Verify empty again
    res5 = client.get("/orders")
    assert res5.get_json() == []
