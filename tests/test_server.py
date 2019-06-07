def test_hello(client, default_data):
    response = client.get('/server/all')
    assert response._status_code == 200
    assert response.content_type == 'application/json'
    assert len(response.data) > 10
