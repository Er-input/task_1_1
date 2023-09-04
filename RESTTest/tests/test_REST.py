import requests
from faker import Faker

def random_user():
    fake = Faker()
    username = fake.email()
    password = fake.password()
    return {"userName": username, "password": password}

class TestAutorized:

    def test_autorization(self):
        body = {"userName": "bublalexxx11@mail.ru", "password": "zxzx1212Z!"}
        response = requests.post("https://demoqa.com/Account/v1/Authorized", json=body)
        assert response.status_code == 200

    def test_uncorrect_data(self):
        body = {"userName": "bublalexxx11@mail.u", "password": "zxzx1212Z!"}
        response = requests.post("https://demoqa.com/Account/v1/Authorized", json=body)
        assert response.status_code == 404
        assert response.json().get('code') == '1207'
        assert response.json().get('message') == 'User not found!'


class TestGenerateToken:

    def test_generate_token(self):
        body = {"userName": "bublalexxx11@mail.ru", "password": "zxzx1212Z!"}
        response = requests.post("https://demoqa.com/Account/v1/GenerateToken", json=body)
        assert response.status_code == 200
        assert response.json().get('status') == 'Success'

    def test_generate_token_with_uncorrect_data(self):
        body = {"userName": "bublalexxx11@mail.u", "password": "zxzx1212Z!"}
        response = requests.post("https://demoqa.com/Account/v1/GenerateToken", json=body)
        assert response.status_code == 200
        assert response.json().get('status') == 'Failed'
        assert response.json().get('token') == None


class TestAddaAndDeleteUser:

    body = random_user()

    def test_user(self):
        response = requests.post("https://demoqa.com/Account/v1/User", json=self.body)
        assert response.status_code == 201
        requests.post("https://demoqa.com/Account/v1/Authorized", json=self.body)
        return response.json().get('userId')

    def test_user_exist(self):
        body = {"userName": "bublalexxx11@mail.ru", "password": "zxzx1212Z!"}
        response = requests.post("https://demoqa.com/Account/v1/User", json=body)
        assert response.status_code == 406
        assert response.json().get('message') == 'User exists!'
        assert response.json().get('code') == '1204'