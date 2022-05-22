from lib.my_requests import Book, URL
import pytest

INVALID_USERNAME = ['', 'test1']
INVALID_PASSWORD = ['', 'test1']


class TestLogin:
    """Тестируем аутентификацию (Login). Валидные данные для входа username = test, password = test"""

    def test_auth_with_valid_data(self):
        session = Book.create_session('test', 'test')
        response = session.get(f"{URL}/search")
        assert response.status_code == 200, \
            f'Wrong response status_code. expected: 200, actual {response.status_code}.'
    @pytest.mark.parametrize('username', INVALID_USERNAME)
    def test_auth_with_invalid_username(self, username):
        session = Book.create_session(username)
        response = session.get(f"{URL}/search")
        assert response.status_code == 401, \
            f'Wrong response status_code. expected: 401, actual {response.status_code}.' \
            f'\n User is logged in with Username: {username}, password: test'

    @pytest.mark.parametrize('password', INVALID_PASSWORD)
    def test_auth_with_invalid_username(self, password):
        session = Book.create_session(password=password)
        response = session.get(f"{URL}/search")
        assert response.status_code == 401, \
            f'Wrong response status_code. expected: 401, actual {response.status_code}.' \
            f'\n User is logged in with Username: test, password: {password}'


class TestLogout:
    def test_logout(self):
        session = Book.create_session()
        Book.logout(session)
        response = session.get(f"{URL}/search")
        assert response.status_code == 401, \
            f'Wrong response status_code. expected: 401, actual {response.status_code}.'
