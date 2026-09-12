from password_utils import derive_key

password = "MySecret123"

salt = b"1234567890123456"

key1 = derive_key(password, salt)
key2 = derive_key(password, salt)

print(key1)
print(key2)

print(key1 == key2)