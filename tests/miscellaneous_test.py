import requests

url = "http://127.0.0.1:5000"

def test_patch():
    response = requests.patch(f"{url}/api/user/update/test@gmail.com", data={"passkey": "test_passkey", "firstName": "test first name", "lastName": "test last name"})
    print(response.json())

test_patch()