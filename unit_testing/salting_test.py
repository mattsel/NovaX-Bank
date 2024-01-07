import unittest
import random
import hashlib

# Generate a random salt for password hashing.
def generate_salt():
    return str(random.randint(100000, 999999))

# Hash the password using SHA-256 algorithm and the provided salt.
def hash_password(password, salt):
    hashed_password = hashlib.sha256((password + str(salt)).encode()).hexdigest()
    return hashed_password

class SaltTesting(unittest.TestCase):
    def test_generate_salt(self):
        self.assertTrue(generate_salt()) #Make sure salt not empty

    def test_hash_password(self):
        password1="password123" #Test password 1 
        salt = generate_salt() #Generate salt
        password2 = 'Password123' #Test password 2 

        hashed_password1 = hash_password(password1, salt) #Salted password 1 
        hashed_password2 = hash_password(password2, salt) #Salted password 2 

        self.assertTrue(hashed_password1 != hashed_password2) #Salted 1 != 2
        self.assertFalse(hashed_password1 == hashed_password2) #Salted 1 == 2

        #Following will test to make sure the same password and salt will create same hashed salt. 
        password_same1 = hash_password("password123", salt) #Same salted as password 1 
        password_same2= hash_password("Password123", salt) #Same salted as password 2

        self.assertTrue(hashed_password1 == password_same1) #Ensure same salt and password give same salted hash password 1 
        self.assertTrue(hashed_password2 == password_same2) #Ensure same salt and password give same salted hash password 2 
        self.assertFalse(hashed_password1 == password_same2) #Cross check to ensure hashed salt password 1 & 2 are not the same
        self.assertFalse(hashed_password2 == password_same1) #Cross check to ensure hashed salt password 1 & 2 are not the same
