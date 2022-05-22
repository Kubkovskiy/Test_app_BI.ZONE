from requests import Response, get, post, Session

URL = 'http://localhost:8080/api/book'
URL_LOGIN = 'http://localhost:8080/api/account/login'
URL_LOGOUT = 'http://localhost:8080/api/account/logout'
VALID_DATA = {"title": 'Valid Title', "isbn": '1234567890123', "categoryId": 1, "formatId": 1}


class Book:
    SESSION = None

    @staticmethod
    def create_session(username: str = 'test', password: str = 'test') -> Session:
        data = {'username': username, 'password': password}
        session = Session()
        session.post(URL_LOGIN, data=data)
        return session

    @classmethod
    def create_session_before_start_testing(cls, username: str = 'test', password: str = 'test'):
        """Create Session, and save in Book.SESSION if not created"""
        if not cls.SESSION:
            cls.SESSION = cls.create_session(username, password)

    @staticmethod
    def logout(session: Session):
        session.post(URL_LOGOUT)

    @staticmethod
    def new_book(json: dict) -> Response:
        return Book.SESSION.post(f"{URL}/new", json=json)

    @staticmethod
    def edit_book(json: dict) -> Response:
        return Book.SESSION.post(f"{URL}/edit", json=json)

    @staticmethod
    def search_book(title: str = None) -> Response:
        query = {'query': title} if title else None
        return Book.SESSION.get(f"{URL}/search", params=query)

    @staticmethod
    def search_book_by_id(book_id: int) -> Response:
        query = {'id': book_id}
        return Book.SESSION.get(f"{URL}", params=query)

    @staticmethod
    def delete_book(data) -> Response:
        return Book.SESSION.post(f"{URL}/delete", json=data)
