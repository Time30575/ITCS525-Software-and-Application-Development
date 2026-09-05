from fastapi.testclient import TestClient
from main import app  # or whatever your app module is

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", json={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", json={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", json={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", json={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""


# TODO Add more tests, 3 per api
# 3 test case for: GET /history
def test_get_history_empty():
    """Case 1: Verify history returns an empty list if we clear it first."""
    client.delete("/history")  # Reset state
    response = client.get("/history")
    assert response.status_code == 200
    assert response.json() == []  # Should be an empty list


def test_get_history_saves_calculation():
    """Case 2: Verify history accurately saves and retrieves a calculation."""
    client.delete("/history")
    
    # Add a calculation
    client.post("/calculate", json={"expr": "15 + 5"})
    
    response = client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["expr"] == "15 + 5"
    assert data[0]["result"] == "20"


def test_get_history_limit_parameter():
    """Case 3: Verify the ?limit query parameter works to restrict items."""
    client.delete("/history")
    
    # Add two separate calculations
    client.post("/calculate", json={"expr": "1+1"})
    client.post("/calculate", json={"expr": "2+2"})
    
    # Ask for only 1 item
    response = client.get("/history", params={"limit": 1})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["expr"] == "2+2"  # Newest item should come first


# 3 test case for: DELETE /history
def test_delete_history_response():
    """Case 4: Verify the delete endpoint responds with a successful JSON format."""
    response = client.delete("/history")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "message" in data


def test_delete_history_clears_populated_list():
    """Case 5: Verify that clearing a full history actually removes all items."""
    # Add some calculations to fill it up
    # client.post("/calculate", params={"expr": "5 * 5"})   ## lec2 markdown
    # client.post("/calculate", params={"expr": "10 / 2"})  ## lec2 markdown
    client.post("/calculate", json={"expr": "5 * 5"})
    client.post("/calculate", json={"expr": "10 / 2"})
    
    # Delete everything
    delete_response = client.delete("/history")
    assert delete_response.status_code == 200
    
    # Fetch history again to ensure it is completely wiped out
    get_response = client.get("/history")
    assert len(get_response.json()) == 0


def test_delete_history_when_already_empty():
    """Case 6: Verify deleting history when it is already empty works safely without crashing."""
    client.delete("/history")  # First clear
    
    # Second clear immediately after
    response = client.delete("/history")
    assert response.status_code == 200
    assert response.json()["ok"] is True


## Lec3 update test on both new API
def test_history_returns_calculator_logs():
    client.delete("/history")

    client.post("/calculate", json={"expr": "15 + 5"})

    response = client.get("/history")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["expr"] == "15 + 5"
    assert data[0]["result"] == "20"
    assert "timestamp" in data[0]