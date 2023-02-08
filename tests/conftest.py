# setup functions called fixtures that each test will use
# tests are in python module that start with test_, and 
# each test function in those modules also starts with test_

# Pytest uses fixtures by matching their function names 
# with the names of arguments in the test functions. 
# For example, the test_hello function you’ll write next takes a client argument. 
# Pytest matches that with the client fixture function, calls it, and 
# passes the returned value to the test function.


"""

python3 -m pytest

test_ 로 시작하는 파일들을 검사. 

conftest.py
테스트에 사용할 인스턴스를 만들어주는 역할을함

@pytest.fixture
test 함수의 인자에 해당하는 인스턴스를 만들어줌. 예로 test 함수 중에서
app 이라는 인자를 받으면 app() 함수 리턴값을 사용한다.
"""

import os
import tempfile

from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db
from werkzeug.test import TestResponse

# 프로세스가 종료되면서 자동으로 자원을 반납할 수 있는 문법
# 파일 입출력때 사용함 
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path # instance 폴더를 사용하지 않고 임시 폴더에 database를 생성한다
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app # 결과값을 여러번 나누어서 제공할 수 있는 리턴 방법

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client: FlaskClient):
        self._client = client
    def login(self, username="test", password="test") -> TestResponse:
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    def logout(self) -> TestResponse:
        return self._client.get('/auth/logout')
    
@pytest.fixture
def auth(client):
    return AuthActions(client)

