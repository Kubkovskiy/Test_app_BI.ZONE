import requests

from lib.my_requests import MyRequests

s = MyRequests.auth('account/login', {'username': 'test', 'password':'test'})
cookies = s.cookies

response = MyRequests.get('book/search', cookies=cookies)
VALID_JSON_DATA = {"title": 'Valid Title', "isbn": '1234567890123', "categoryId": 1, "formatId": 1}
content = response.json()

for i in content['content']:
    delete = requests.post('http://localhost:8080/api/book/delete', cookies=cookies, json=i)
    delete.text

data = {"id":2,"title":"Valid Title","isbn":"1234567890123","categoryId":1,"formatId":1}

#
# resp_post = MyRequests.post('book/new', cookies=cookies, data=VALID_JSON_DATA)
# print(type(resp_post.json()))