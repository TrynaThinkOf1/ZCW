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

def test_verify():
    response = requests.get(f"{url}/api/user/verify/fosterdraws@gmail.com")
    print(response)
    code = input("Enter verification code: ")
    response = requests.post(f"{url}/api/code/verify/{code}", data={"firstName": "Foster", "lastName": "Berlin", "email": "fosterdraws@gmail.com",
    "passkey": "testPasskey2", "displayName": "Super Awesome Cool Girl"})
    print(response.json())

test_verify()