import unittest

# Check if the password meets the minimum length requirement.
def pass_length(password):
    return len(password) >= 6 and ' ' not in password

# Check if the password contains at least one uppercase letter.
def pass_capital(password):
    return any(char.isupper() for char in password)

# Check if the password contains at least one special character.
def pass_special(password):
    special = "!@#$%^&*()-+?_=,<>/."
    return any(char in special for char in password)

# Check if the password contains at least one numerical digit.
def pass_numerical(password):
    numerical = "0123456789"
    return any(char in numerical for char in password)

class TestPasswordValidation(unittest.TestCase):
    def test_pass_length(self):
        self.assertTrue(pass_length('Hello_World'))  # Password length > 6
        self.assertTrue(pass_length('Helllo'))  # Password length > 6
        self.assertFalse(pass_length('Hello'))  # Password length <= 6
        self.assertFalse(pass_length("Hello World"))  # Password length <= 6
    def test_pass_capital(self):
        self.assertTrue(pass_capital("Hello_World")) #Passworld has capital
        self.assertFalse(pass_capital("hello_world")) #Password doesn't have capital
    def test_pass_special(self):
        self.assertTrue(pass_special("Hello_world")) #Password has special char
        self.assertFalse(pass_special("Hello World")) #Password doesn't have special char
    def test_pass_numerical(self):
        self.assertTrue(pass_numerical("Hello_world123")) #Password has numerical
        self.assertFalse(pass_numerical("Hello_world")) #Password doesn't have numerical
if __name__ == '__main__':
    unittest.main()