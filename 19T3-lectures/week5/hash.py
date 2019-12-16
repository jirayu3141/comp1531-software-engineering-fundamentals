import hashlib
print("mypassword")
print("mypassword".encode())
print(hashlib.sha256("mypassword".encode()))
print(hashlib.sha256("mypassword".encode()).hexdigest())
