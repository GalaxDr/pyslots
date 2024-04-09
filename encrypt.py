from cryptography.fernet import Fernet
import json


def generate_key():
    return Fernet.generate_key()


def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text


def decrypt_data(cipher_text, key):
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text).decode()
    return plain_text


encryption_key = generate_key()
with open("encryption_key.key", "wb") as key_file:
    key_file.write(encryption_key)

data = {
    "admin": {
    "id": 1,
    "name": "admin",
    "balance": 100,
    "password": "admin",
    "admin": "yes"
  },
  "johnd": {
    "id": 2,
    "name": "John Dana",
    "balance": 100,
    "password": "1234",
    "admin": "no"
  },
  "joana": {
    "id": 3,
    "name": "Joana Black",
    "balance": 100,
    "password": "12345",
    "admin": "no"
  },
  "pedro": {
    "id": 4,
    "name": "Pedro Franck",
    "balance": 99,
    "password": "bicicleta123",
    "admin": "no"
  }
}

json_data = json.dumps(data)
encrypted_data = encrypt_data(json_data, encryption_key)

with open("users_encrypted.json", "wb") as encrypted_file:
    encrypted_file.write(encrypted_data)

with open("users_encrypted.json", "rb") as encrypted_file:
    encrypted_data = encrypted_file.read()

decrypted_data = decrypt_data(encrypted_data, encryption_key)
json_data = json.loads(decrypted_data)
print(json_data)