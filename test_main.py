from fastapi.testclient import TestClient
from main import app  # or whatever your app module is

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""


# TODO Add more tests
def test_basic_multiplication():
    # Tests a simple multiplication problem
    r = client.post("/calculate", params={"expr": "5 * 6"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["result"] == 30


def test_basic_addition_with_spaces():
    # Tests that adding numbers with whitespace works perfectly
    r = client.post("/calculate", params={"expr": "12 + 8"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["result"] == 20


def test_clear_history_endpoint():
    # Tests that the delete history route returns a success response
    r = client.delete("/history")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True