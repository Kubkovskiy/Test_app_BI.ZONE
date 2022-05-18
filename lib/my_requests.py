import requests


class MyRequests:

    @staticmethod
    def auth(uri: str, data: dict = None):
        return MyRequests._send(uri, data, method='AUTH')

    @staticmethod
    def post(uri: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(uri, data, headers, cookies, "POST")

    @staticmethod
    def get(uri: str, params: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(uri, params, headers, cookies, method="GET")

    @staticmethod
    def delete(uri: str, data: dict = None, cookies: dict = None):
        return MyRequests._send(uri, data, method="DELETE")

    @staticmethod
    def _send(uri: str, data: (dict, list) = None, headers: dict = None, cookies: dict = None,
              method: str = None):

        url = f"http://localhost:8080/api/{uri}"
        if headers is None:
            headers = {}


        if method == "GET":
            response = requests.get(url, params=data, headers=headers, cookies=cookies)

        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, cookies=cookies)

        elif method == "DELETE":
            response = requests.post(url, params=data, cookies=cookies)

        elif method == "AUTH":
            response = requests.Session().post(url, params=data)

        else:
            raise Exception(f"Bad http method '{method}' was received")

        return response
