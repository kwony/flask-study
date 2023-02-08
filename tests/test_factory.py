from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

# conftest.py 에서 선언된 client 메써드의 결과를 사용한다.
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'