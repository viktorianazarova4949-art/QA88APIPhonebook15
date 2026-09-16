import pytest

from config import *


class TestLogin:

    def test_login_positive(self, session, login_url, registered_user):
        body = {
            "username": registered_user.username,
            "password": registered_user.password,
        }
        headers = {"Content-Type": "application/json"}
        response = session.post(login_url, json=body, headers=headers)
        assert response.status_code == 200
        assert "token" in response.json().keys()

    @pytest.mark.parametrize("invalid_username", [
        "",
        "dfrty678@rty.bn"
    ])
    def test_login_negative_wrong_email(self, session, login_url, invalid_username):
        body = {
            "username": invalid_username,
            "password": TEST_PASSWORD,
        }
        response = session.post(login_url, json=body)
        print(response.json())
        assert response.status_code in [401, 403]
        assert "Login or Password incorrect" in response.json().values()

    @pytest.mark.parametrize("invalid_password", [
        "",
        "Qwert345!"
    ])
    def test_login_negative_wrong_password(self, session, login_url, invalid_password):
        body = {
            "username": TEST_EMAIL,
            "password": invalid_password,
        }
        response = session.post(login_url, json=body)
        print(response.json())
        assert response.status_code == 401
        assert "Login or Password incorrect" in response.json().values()