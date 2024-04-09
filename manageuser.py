import json
import os
from cryptography.fernet import Fernet


def main():
    print("1 - Add user")
    print("2 - Delete user")
    print("3 - Manage users")
    print("4 - Exit")
    choice = input("Select an option:")
    match choice:
        case "1":
            add_new_user()
        case "2":
            exclude_user()
        case "3":
            manage_users()
        case "4":
            exit()
        case _:
            print("Invalid input")


def admin_login():
    with open('users_encrypted.json', 'rb') as f:
        encrypted_data = f.read()

    encryption_key = os.getenv("KEY")
    decrypted_data = decrypt_data(encrypted_data, encryption_key)
    users = json.loads(decrypted_data)

    username = input("Enter a username:")
    if username in users:
        password = input("Enter a password:")
        if password == users[username]["password"]:
            if users[username]["admin"] == "yes":
                return username
            else:
                print("You are not an admin")
                admin_login()
        else:
            print("Incorrect password")
            admin_login()
    else:
        print("User not found")
        admin_login()


def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text


def decrypt_data(cipher_text, key):
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text).decode()
    return plain_text


def add_new_user():
    with open('users_encrypted.json', 'rb') as f:
        encrypted_data = f.read()

    encryption_key = os.getenv("KEY")
    decrypted_data = decrypt_data(encrypted_data, encryption_key)
    users = json.loads(decrypted_data)

    username = input("Enter a username:")
    if username in users:
        print("Username already exists")
        add_new_user()
    else:
        password = input("Enter a password:")
        name = input("Enter your name:")
        users[username] = {"id": len(users) + 1, "name": name, "balance": 100, "password": password,
                           "admin": "no"}

        with open('users_encrypted.json', 'wb') as f:
            encrypted_data = encrypt_data(json.dumps(users), os.getenv("KEY"))
            f.write(encrypted_data)

        print("User created")


def exclude_user():
    admin_login()

    with open('users_encrypted.json', 'rb') as f:
        encrypted_data = f.read()

    encryption_key = os.getenv("KEY")
    decrypted_data = decrypt_data(encrypted_data, encryption_key)
    users = json.loads(decrypted_data)

    username = input("Enter a username:")
    if username in users:
        del users[username]

        with open('users_encrypted.json', 'wb') as f:
            encrypted_data = encrypt_data(json.dumps(users), os.getenv("KEY"))
            f.write(encrypted_data)

        print("User deleted")
    else:
        print("User not found")


def manage_users():
    admin_login()
    with open('users_encrypted.json', 'rb') as f:
        encrypted_data = f.read()

    encryption_key = os.getenv("KEY")
    decrypted_data = decrypt_data(encrypted_data, encryption_key)
    users = json.loads(decrypted_data)

    choice = input("1 - Print all users\n2 - Print all details\n3 - Change balance\nSelect an option:")
    match choice:
        case "1":
            for user in users:
                print(user)
        case "2":
            for user in users:
                print(user)
                for key, value in users[user].items():
                    print(key, ":", value)
                print("----------")
        case "3":
            change_user_balance()
        case _:
            print("Invalid input")


def change_user_balance():
    with open('users_encrypted.json', 'rb') as f:
        encrypted_data = f.read()

    encryption_key = os.getenv("KEY")
    decrypted_data = decrypt_data(encrypted_data, encryption_key)
    users = json.loads(decrypted_data)

    username = input("Enter a username:")
    if username in users:
        print(f"Current balance: {users[username]['balance']}")
        balance = int(input("Enter a new balance:"))
        users[username]["balance"] = balance

        with open('users_encrypted.json', 'wb') as f:
            encrypted_data = encrypt_data(json.dumps(users), os.getenv("KEY"))
            f.write(encrypted_data)
        print("Balance changed")
    else:
        print("User not found")


if __name__ == '__main__':
    main()
