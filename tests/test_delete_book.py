from lib.my_requests import Book, VALID_DATA


class TestDelete:
    """ISBN Номер должен состоять из 10 или 13 ЦИФР, и быть уникальным"""

    def test_delete_book(self):
        data_after_create_book = Book.new_book(VALID_DATA).json()
        delete_book = Book.delete_book(data_after_create_book)
        assert delete_book.status_code == 200, \
            f'Wrong response status_code. expected: 200, actual {delete_book.status_code}.' \
            f' Card not deleted'

    def test_is_deleted_book_in_db(self):
        created_book = Book.new_book(VALID_DATA).json()
        Book.delete_book(created_book)
        book_id = Book.search_book_by_id(created_book['id']).json()['id']
        assert book_id == 0, f"Book didn't delete form DB. actual id: {book_id}"
