import os
import bcrypt

os.system('clear')

pwd_value = input('Type value to encrypt: ')
pw = pwd_value.encode('utf-8')
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(pw, salt)
print("Hashed value: " + str(hashed))
