import requests

data2 = {
        'first_name': 'Papa',
        'last_name': 'Kingsley',
        'username': 'admin',
        'vehicle_number': 'sRaymond',
        'email': 'admin@delivery.com',
        'password': 'password',
        'phone_number': '4321456',
        'status': 'busy',
        }

# headers = {'Content-Type': 'multipart/form-data'}
# headers = {'Content-Type': 'application/json'}
info = requests.post('http://localhost:5000/api/register', data=data2)
# data3 = {
#    'email': 'admin@delivery.com',
#    'password': '112345'
#     }
print(info.json())
# response = requests.post('http://localhost:5000/api/forgot_password', data=data3)
# # token = response.json().get('success', None)
# print(token, "\n I am the token")
# data4 = {
#         'email': 'dominicmorba@gmail.com',
#             'password': 'domnic',
#             'token': token
#         }