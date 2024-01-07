import unittest
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime

# Get hidden databse URL from .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env') 
load_dotenv(dotenv_path) 

# Connect to database using flask
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)

# Function that defines data types and columns in table 'User'
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(6), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0)

# Function that defines data types and columns in table 'CreditApplications'
class CreditApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    annual_income = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Function that defines data types and columns in table 'Transaction'
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class database_test(unittest.TestCase):
    def user_table_test(self):
        test_user_data = {
            'username': 'user_unittesting',
            'email': 'user_unittesting@gmail.com',
            'password': 'user_1234567',
            'salt': 'user_1',
            'balance': 200
        }

        # Create new user instance
        test_user=User(**test_user_data)

        # Add user to memory
        db.session.add(test_user)
        db.session.commit()

        # Retrive user from database
        retrieved_user=User.query.filter_by(username='test_user').first()
        self.assertIsNotNone(retrieved_user)

        # Assert that the attributes match
        self.assertEqual(retrieved_user.username, test_user_data['username'])
        self.assertEqual(retrieved_user.email, test_user_data['email'])
        self.assertEqual(retrieved_user.password, test_user_data['password'])
        self.assertEqual(retrieved_user.salt, test_user_data['salt'])
        self.assertEqual(retrieved_user.balance, test_user_data['balance'])
        
        # Clear up database after test
        db.session.delete(retrieved_user)
        db.session.commit()

    def CreditApplication_table_test(self):
        test_credit_data = {
            'first_name': 'firstName_unittesting',
            'last_name': 'lastName_unittesting',
            'email': 'email_unittesting@gmail.com',
            'address': '123 unittesting ln',
            'city': 'Philadelphia',
            'state': 'Pennsylvania',
            'postal_code': '19145',
            'annual_income': 50000,
        }
        # Create new user instance
        test_credit=User(**test_credit_data)

        # Add user to memory
        db.session.add(test_credit)
        db.session.commit()

        # Retrieve user from database
        retrieved_credit = CreditApplication.query.filter_by(email='email_unittesting@gmail.com').first()

        # Assert attributes match databse
        self.assertEqual(retrieved_credit.first_name, test_credit_data['first_name'])
        self.assertEqual(retrieved_credit.last_name, test_credit_data['last_name'])
        self.assertEqual(retrieved_credit.email, test_credit_data['email'])
        self.assertEqual(retrieved_credit.address, test_credit_data['address'])
        self.assertEqual(retrieved_credit.city, test_credit_data['city'])
        self.assertEqual(retrieved_credit.state, test_credit_data['state'])
        self.assertEqual(retrieved_credit.postal_code, test_credit_data['postal_code'])
        self.assertEqual(retrieved_credit.annual_income, test_credit_data['annual_income'])

        # Clean up database after test
        db.session.delete(retrieved_credit)
        db.session.commit()

    def transaction_table_test(self):
        test_transaction_data = {
            'user_email': 'unittest_transaction@gmail.com',
            'transaction_type': 'Deposit',
            'amount': 200
        }

        # Create new user instance
        test_transaction=User(**test_transaction_data)

        # Add user to memory
        db.session.add(test_transaction)
        db.session.commit()

        #Retrieve user from database
        retrieved_transaction = Transaction.query.filter_by(user_email='unittest_transaction@gmail.com').first()

        # Assert Attributes Match
        self.assertEqual(retrieved_transaction.user_email, test_transaction_data['user_email'])
        self.assertEqual(retrieved_transaction.transaction_type, test_transaction_data['transaction_type'])
        self.assertEqual(retrieved_transaction.amount, test_transaction_data['amount'])

        # Clean up database after test
        db.session.delete(retrieved_transaction)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()