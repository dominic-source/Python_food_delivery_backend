import requests

# data2 = {
#         'first_name': '1Loveth',
#         'last_name': '1Ubah',
#         'username': '1sdominic',
#         'vehicle_number': 'sRaymond',
#         'email': '1dominicmorba@gmail.com',
#         'password': '112345',
#         'phone_number': '1233455632',
#         'status': 'busy',
#         }

# # headers = {'Content-Type': 'multipart/form-data'}
# # headers = {'Content-Type': 'application/json'}
# info = requests.post('http://localhost:5000/api/register', data=data2)
data3 = {
   'email': 'dominicmorba@gmail.com',
   'password': '112345'
    }
# print(info.json())
response = requests.post('http://localhost:5000/api/forgot_password', data=data3)
token = response.json().get('success', None)
print(token, "\n I am the token")
# data4 = {
#         'email': 'dominicmorba@gmail.com',
#             'password': 'domnic',
#             'token': token
#         }