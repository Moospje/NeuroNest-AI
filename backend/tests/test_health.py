def test_health_check(client):
    """
    Test that the health check endpoint returns a 200 status code.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}