import jwt

encoded_jwt = jwt.encode({'some': 'payload'}, 'applepineappleorange', algorithm='HS256')

print(jwt.decode(encoded_jwt, 'applepineappleorange', algorithms=['HS256']))