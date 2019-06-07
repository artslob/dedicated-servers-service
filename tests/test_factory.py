def test_hello(client):
    response = client.get('/')
    assert response.data == b'index page'
