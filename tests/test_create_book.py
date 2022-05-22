from lib.my_requests import Book, VALID_DATA
import pytest

VALID_ISBN = ['1' * 10, '2' * 13]
INVALID_ISBN = ['1' * 9, '2' * 11, '3' * 14, ' ', '!@#$%^&*()9=', '1a' * 5]
VALID_TITLE = ['A' * 3, 'a' * 50, 'a' * 25, '123' * 10, 'Valid !@#$%^&*()']
INVALID_TITLE = ['12', 'a' * 51, '', ' ' * 25]


class TestIsbn:
    """ISBN Номер должен состоять из 10 или 13 ЦИФР(int), и быть уникальным"""

    @pytest.mark.parametrize('valid_isbn', VALID_ISBN)
    def test_create_book_with_valid_isbn(self, valid_isbn):
        data = VALID_DATA.copy()
        data["isbn"] = valid_isbn
        response = Book.new_book(data)
        expected_status_code = 200
        assert response.status_code == expected_status_code, \
            f'Wrong response status_code. expected: {expected_status_code}, actual {response.status_code}.' \
            f'isbn: {valid_isbn} not suitable'

    @pytest.mark.parametrize('invalid_isbn', INVALID_ISBN)
    def test_create_book_with_invalid_isbn(self, invalid_isbn):
        data = VALID_DATA.copy()
        data["isbn"] = invalid_isbn
        response = Book.new_book(data)
        expected_status_code = 400
        assert response.status_code == expected_status_code, \
            f'Wrong response status_code. expected: {expected_status_code}, actual {response.status_code}.' \
            f'Card with isbn: {invalid_isbn} created, length of isbn:{len(invalid_isbn)}.'

    def test_create_book_with_same_isbn(self):
        response = Book.new_book(VALID_DATA)
        response2 = Book.new_book(VALID_DATA)
        expected_status_code = 400
        assert response2.status_code == expected_status_code, \
            f'Wrong response status_code. expected: {expected_status_code}, actual {response2.status_code}.' \
            f'Card with same isbn created: ISBN: {VALID_DATA["isbn"]}'


class TestTitle:
    """Поле Title должно быть длиной от 3 до 50 символов, не должно состоять только из пробелов"""

    @pytest.mark.parametrize('valid_title', VALID_TITLE)
    def test_create_book_with_valid_title(self, valid_title):
        data = VALID_DATA.copy()
        data["title"] = valid_title
        response = Book.new_book(data)
        expected_status_code = 200
        assert response.status_code == expected_status_code, \
            f'Wrong response status_code. expected: {expected_status_code}, actual {response.status_code}.\
             title: {valid_title} not suitable'

    @pytest.mark.parametrize('invalid_title', INVALID_TITLE)
    def test_create_book_with_invalid_title(self, invalid_title):
        data = VALID_DATA.copy()
        data["title"] = invalid_title
        response = Book.new_book(data)
        expected_status_code = 400
        assert response.status_code == expected_status_code, \
            f'Wrong response status_code. expected: {expected_status_code}, actual {response.status_code}.' \
            f' Card with title: {invalid_title} created'

    def test_is_created_book_in_db(self):
        created_book_id = Book.new_book(VALID_DATA).json()['id']
        actual_id = Book.search_book_by_id(created_book_id).json()['id']
        assert created_book_id == actual_id, \
            f"Wrong id, expected:{created_book_id}, actual:{actual_id}"


class TestCategoryAndFormat:
    """Поле Category необязательное (на быбор 3 строки), отправляется в БД по индексу (0,1,2)
    Поле Format также необязатенльное (на выбор 2 строки)"""

    @pytest.mark.parametrize('valid_cat_index', [0, 1, 2])
    def test_create_book_with_valid_category(self, valid_cat_index):
        data = VALID_DATA.copy()
        data["categoryId"] = valid_cat_index
        response = Book.new_book(data)
        expected_status_code = 200
        assert response.status_code == expected_status_code, \
            f'Wrong response status_code. expected: {expected_status_code}, actual {response.status_code}.\
                 categoryId: {valid_cat_index} not suitable'

    @pytest.mark.parametrize('format_index', [0, 1])
    def test_create_book_with_valid_format(self, format_index):
        data = VALID_DATA.copy()
        data["formatId"] = format_index
        response = Book.new_book(data)
        expected_status_code = 200
        assert response.status_code == expected_status_code, \
            f'Wrong response status_code. expected: {expected_status_code}, actual {response.status_code}.\
                     formatId: {format_index} not suitable'
