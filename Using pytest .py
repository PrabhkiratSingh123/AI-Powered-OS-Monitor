import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_system_status(client):
    response = client.get('/api/system_status')
    assert response.status_code == 200
    assert "cpu_usage" in response.json
