import requests
url = " http://127.0.0.1:8000/photo/"


def send_file(base54):
    data = {
        "file": base54
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_TOKEN"
    }
    response = requests.post(url, json=data, headers=headers)
    # print(response.status_code)
    return response.status_code