import json


def test_hello(client, default_data):
    response = client.get('/server/all')
    assert response._status_code == 200
    assert response.content_type == 'application/json'
    servers = json.loads(response.data)
    assert len(servers) == 25
