import requests
# Login airline
url = 'http://127.0.0.1:8000/Login/'

data = {
    'ID': '9166110178323000524',
    # 'Name': 'TestUser2',
    # 'Email': '21111@qq.com',
    'Password': '21123456',

}
session = requests.session()
response = session.post(url, data=data)
print(response.status_code)
print(response.json())


PaymentId = '2117873720697902579'
# refund
url = 'http://127.0.0.1:8000/Refund/'
data = {
    'PaymentId': PaymentId,
    'Price': '1',
}
response = session.post(url, data=data)
print(response.status_code)
print(response.json())

