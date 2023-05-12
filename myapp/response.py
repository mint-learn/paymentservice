import requests

# Regist
url = 'http://127.0.0.1:8000/payment/register/'
data = {
    'Name': 'User',
    'Email': '21111@qq.com',
    'Password': '21123456',
}
response = requests.post(url, data=data)
print(response.status_code)
print(response.json())


# Login airline
url = 'http://127.0.0.1:8000/payment/login/'
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

# Balance
url = 'http://127.0.0.1:8000/payment/balance/'

response = session.post(url, data=data)
print(response.status_code)
print(response.json())

# Deposit
url = 'http://127.0.0.1:8000/payment/deposit/'
data = {
    'Price': '1000',
}
response = session.post(url, data=data)
print(response.status_code)
print(response.json())

# order_request
# {'PaymentId': 2117873720697902579, 'Stamp': '1be62d7675ac4809ace0ce287b474e8a'} 1913145929129894887
url = 'http://127.0.0.1:8000/payment/order/'
data = {
    'MerchantOrderId': '111',
    'Price': '10'}
response = session.post(url, data=data)
print(response.status_code)
print(response.json())
PaymentId = response.json()['PaymentId']
# print(PaymentId)

# Login user
# {'AccountID': 2770548534592511, 'Name': 'User'}
url = 'http://127.0.0.1:8000/payment/login/'

data = {
    'ID': '2770548534592511',
    # 'Name': 'User',
    # 'Email': '21111@qq.com',
    'Password': '21123456',

}
session = requests.session()
response = session.post(url, data=data)
print(response.status_code)
print(response.json())


# payment_request
url = 'http://127.0.0.1:8000/payment/payment/'
data = {
    'PaymentId': PaymentId}
response = session.post(url, data=data)
print(response.status_code)
print(response.json())



# Login airline
url = 'http://127.0.0.1:8000/payment/login/'

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



# refund
url = 'http://127.0.0.1:8000/payment/refund/'
data = {
    'PaymentId': PaymentId,
    'Price': '1',
}
response = session.post(url, data=data)
print(response.status_code)
print(response.json())


# search
url = 'http://127.0.0.1:8000/payment/search/'
data = {
    'pages': 1,
    'EntriesPerPage': '2',
}
response = session.post(url, data=data)
print(response.status_code)
print(response.json())

