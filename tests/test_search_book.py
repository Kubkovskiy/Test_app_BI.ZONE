from lib.my_requests import Book, VALID_DATA
from uuid import uuid4


class TestSearch:

    def test_search_when_bd_is_empty(self, clean_db):
        response = Book.search_book()
        content = response.json()['content']
        assert content is None, f"There are books in the database. {content}"
        data = VALID_DATA.copy()
        data['title'] = str(uuid4())
        Book.new_book(data)

    def test_search_with_unique_title(self):
        data = VALID_DATA.copy()
        data['title'] = str(uuid4())
        Book.new_book(data)
        response = Book.search_book(data['title']).json()['content'][0]
        response_title = response['title']
        assert response_title == data['title'], \
            f"Expected title: {data['title']} not equal actual title: {response_title}"

    def test_search_with_wrong_title(self):
        unique_title = str(uuid4())
        response = Book.search_book(unique_title).json()
        content = response['content']
        assert content is None, f"There are books in the database. {content}"
