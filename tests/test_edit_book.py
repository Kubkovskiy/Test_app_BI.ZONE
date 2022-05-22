from lib.my_requests import Book, VALID_DATA


class TestEditIsbn:

    def test_edit_book_change_title(self):
        edit_title = 'Edit Title'
        created_book_id = Book.new_book(VALID_DATA).json()['id']
        edit_data = {'id': created_book_id, "title": edit_title, "isbn": "1234567890123",
                     "categoryId": 1, "formatId": 1}
        Book.edit_book(edit_data)
        get_book = Book.search_book_by_id(created_book_id).json()
        assert get_book['title'] == edit_title, f'The book was not changed. ' \
            f'Expected title:{edit_title}, actual:{get_book["title"]}.'

    def test_edit_book_change_isbn(self):
        edit_isbn = '1000000000123'
        created_book_id = Book.new_book(VALID_DATA).json()['id']
        edit_data = {'id': created_book_id, "title": 'Valid title', "isbn": edit_isbn,
                     "categoryId": 1, "formatId": 1}
        Book.edit_book(edit_data)
        get_book = Book.search_book_by_id(created_book_id).json()
        assert get_book['isbn'] == edit_isbn, f'The book was not changed. ' \
            f'Expected isbn:{edit_isbn}, actual:{get_book["isbn"]}.'
