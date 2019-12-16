import jwt

SECRET = 'sempai'

encoded_jwt = jwt.encode({'username': 'hayden'}, SECRET, algorithm='HS256')

print(jwt.decode(encoded_jwt, SECRET, algorithms=['HS256']))