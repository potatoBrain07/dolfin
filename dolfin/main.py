from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def generate_key(password):
    salt = b'salt_'  
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt(content, password):
    key = generate_key(password)
    return Fernet(key).encrypt(content)


def decrypt(content, password):
    key = generate_key(password)
    return Fernet(key).decrypt(content)


def main():
    print('''
.----.  .----. .-.   .----..-..-. .-.
| {}  \\/  {}  \\| |   | {_  | ||  `| |
|     /\\      /| `--.| |   | || |\\  |
`----'  `----' `----'`-'   `-'`-' `-'
    ''')

    while(True):
        print("> ",end = "")
        prompt = input()
        words = prompt.split(" ")
        command = words[0]
        if len(words)==3:
            path = words[1]
            passwd = words[2]
            path = path.replace("\\","/")
            path = path.replace("\"","")
            path = path.replace("'","")
        if command == "enc" :
            with open(path, "rb") as file:
                content = file.read()
            content_encrypted = encrypt(content, passwd)
            with open(path, "wb") as file:
                file.write(content_encrypted)
            print("File successfully encrypted.")
        elif command == "dec" :
            with open(path, "rb") as file:
                content = file.read()
            content_decrypted = decrypt(content, passwd)
            with open(path, "wb") as file:
                file.write(content_decrypted)
            print("File successfully decrypted.")
        elif command == "exit" :
            break
        else :
            print(f"Error: \"{command}\" is not a valid command.")

if __name__ == "__main__":
    main()
