import json


from lib.my_requests import MyRequests
from lib.assertions import Assertions

VALID_AUTH_DATA = {'username': 'test', 'password': 'test'}
INVALID_AUTH_DATA = ['test1', '1234567890', '', '!@#$%^&*()']
VALID_JSON_DATA = {"title": 'Valid Title', "isbn": '1234567890123', "categoryId": 1, "formatId": 1}
VALID_ISBN = ['1234567890123']
INVALID_ISBN = ['12345678901234', '1', 'qwe4567890', '!@#$%^&*()']


class TestAuth:

    def test_auth_with_valid_data(self):
        response = MyRequests.auth('account/login', VALID_AUTH_DATA)
        Assertions.assert_expected_status_code(response, 200)
        assert len(response.cookies) != 0, "Response hasn't RequestsCookieJar"

    def test_get_method_after_auth(self):
        response = MyRequests.auth('account/login', VALID_AUTH_DATA)
        cookies = response.cookies
        response_after_auth = MyRequests.get('book/search', cookies=cookies)
        Assertions.assert_expected_status_code(response_after_auth, 200)

    def test_auth_with_invalid_data(self):
        for i in INVALID_AUTH_DATA:
            invalid_pass = {'username': VALID_AUTH_DATA['username'],
                            'password': i}
            response = MyRequests.auth('account/login', invalid_pass)
            Assertions.assert_expected_status_code(response, 401)
            assert len(response.cookies) == 0, "Response has RequestsCookieJar"


class TestCreateMarkdown:

    def test_creat_markdown_with_valid_isnb_and_title(self):
        cookies = MyRequests.auth('account/login', VALID_AUTH_DATA).cookies
        for i in VALID_ISBN:
            response = MyRequests.post('book/new', data=VALID_JSON_DATA, cookies=cookies)
            # Assertions.assert_expected_status_code(response, 201)
            Assertions.assert_json_has_keys(response, ['id', 'title', 'isbn'])
            create_mark_id = response.json()['id']
            response_after_create = MyRequests.get('book/search', cookies=cookies)
            Assertions.assert_expected_status_code(response_after_create, 200)
            content = response_after_create.json()['content']
            last_id_from_response = content[-1]['id']
            assert create_mark_id == last_id_from_response, \
                f"Response ID from POST method = {response_after_create} \
                not equal to ID from GET method : {last_id_from_response}"

    def test_creat_markdown_with_invalid_categories(self):
        cookies = MyRequests.auth('account/login', VALID_AUTH_DATA).cookies
        invalid_json_data = VALID_JSON_DATA
        invalid_json_data['categoryId'] = 5
        response = MyRequests.post('book/new', data=invalid_json_data, cookies=cookies)
        # Assertions.assert_expected_status_code(response, 400)
        Assertions.assert_json_has_keys(response, ['id', 'title', 'isbn'])
        create_mark_id = json.loads(response.content)['id']

        response_after_create = MyRequests.get('book/search', cookies=cookies)
        Assertions.assert_expected_status_code(response_after_create, 200)
        content = response_after_create.json()['content']
        last_id_from_response = content[-1]['id']
        # assert create_mark_id == last_id_from_response, \
        #     f"Response ID from POST method = {response_after_create} \
        #     not equal to ID from GET method : {last_id_from_response}"


class TestDeleteMarkdown:

    def test_delete_markdown(self):
        cookies = MyRequests.auth('account/login', VALID_AUTH_DATA).cookies
        response = MyRequests.post('book/new', data=VALID_JSON_DATA, cookies=cookies)
        response_data = response.json()
        Assertions.assert_json_has_keys(response, ['id', 'title', 'isbn'])
        response_after_delete = MyRequests.post('book/delete', data=response_data, cookies=cookies)
        get_response = MyRequests.get('book/search', cookies=cookies)
        all_markdowns_id = [markdown['id'] for markdown in get_response.json()['content']]
        deleted_markdown_id = response.json()['id']
        assert deleted_markdown_id not in all_markdowns_id, 'deleted card data still in the database'


class TestSearchMarkdown:

    def test_search_markdown_without_any_params(self):
        cookies = MyRequests.auth('account/login', VALID_AUTH_DATA).cookies
        count = 1
        valid_data = VALID_JSON_DATA
        my_title = []
        for i in range(5):
            title = "Valid Title" + str(count)
            valid_data['title'] = title
            response = MyRequests.post('book/new', data=valid_data, cookies=cookies)
            count += 1
            my_title.append(title)
        get_response = MyRequests.get('book/search', cookies=cookies)
        Assertions.assert_expected_status_code(get_response, 200)
        all_markdowns_title = [markdown['title'] for markdown in get_response.json()['content']]
        for text in my_title:
            assert text in all_markdowns_title, f'there is no title {text} in the database'

        # set current title for search
        query = {'query': 'Valid Title1'}
        get_response = MyRequests.get('book/search', params=query, cookies=cookies)
        Assertions.assert_expected_status_code(get_response, 200)
        content = get_response.json()['content']
        for markdown in content:
            assert query['query'] in markdown['title'], \
                f'Wrong title! expected {query["query"]}, actual{markdown["title"]}'
