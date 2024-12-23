import requests

url = "http://127.0.0.1:5000"

def test_patch():
    response = requests.patch(f"{url}/api/user/update/zeviberlin@gmail.com", data={"passkey": "thisIsNotARealPasskey", "phoneNumber": "1234567890"})
    print(response.json())

def test_post():
    response = requests.post(f"{url}/api/user/create", data={"firstName": "Zevi", "lastName": "Berlin", "email": "zeviberlin@gmail.com",
    "passkey": "thisIsNotARealPasskey", "displayName": "TrynaThinkOf1", "bio": "I am the creator of this API!", "website": "https://www.github.com/TrynaThinkOf1"})
    print(response.json())

def test_delete():
    response = requests.delete(f"{url}/api/user/delete/zeviberlin@gmail.com", data={"passkey": "thisIsNotARealPasskey"})
    print(response.json())

test_delete()