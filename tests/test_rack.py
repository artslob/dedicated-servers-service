import json


def test_racks_all(client, default_data):
    response = client.get('/rack/all')
    assert response._status_code == 200
    assert response.content_type == 'application/json'
    racks = json.loads(response.data)
    assert len(racks) == 2
