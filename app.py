from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import hashlib
import re
import random
import logging
from dotenv import load_dotenv
import os

#Sample Login Credentials
#test_user@gmail.com
#Test_user123

#test_wire@gmail.com
#Test_wire123

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'b8f33c292e6f449a0d53e8c376ea6f13'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize Database Connection
mydb = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    passwd=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME')
)
mycursor = mydb.cursor()

# SQL formula to insert new user information, and transaction information
sqlFormula = "INSERT INTO information (username, email, password, salt, balance) VALUES (%s, %s, %s, %s, %s)"
transactionFormula = "INSERT INTO transactions (user_email, transaction_type, amount) VALUES (%s, %s, %s)"

# Retrieve user balance from the database.
def get_balance(email):
    mycursor.execute("SELECT balance FROM information WHERE email = %s", (email,))
    return mycursor.fetchone()[0]

# Retrieve username associated with the given email.
def get_username(email):
    mycursor.execute("SELECT username FROM information WHERE email = %s", (email,))
    return mycursor.fetchone()[0]

# Check if a user with the given email exists in the database.
def check_user_exists(email):
    mycursor.execute("SELECT COUNT(*) FROM information WHERE email = %s", (email,))
    count = mycursor.fetchone()[0]
    return count > 0

# Check if the password and confirm password match.
def pass_check(request):
    password = request.form.get('password')
    conf_password = request.form.get('confirm_password')
    if password != conf_password:
        return "Please confirm your passwords match"
    else:
        return password

# Check if the password meets the minimum length requirement.
def pass_length(password):
    return len(password) > 6

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

# Generate a random salt for password hashing.
def generate_salt():
    return str(random.randint(100000, 999999))

# Hash the password using SHA-256 algorithm and the provided salt.
def hash_password(password, salt):
    hashed_password = hashlib.sha256((password + str(salt)).encode()).hexdigest()
    return hashed_password

@app.route('/')
# Render the index page.
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
# Handle user login by checking if an account exists. 
def login():
    error_message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        mycursor.execute("SELECT salt FROM information WHERE email = %s", (email,))
        salt_data = mycursor.fetchone()

        if salt_data:
            salt_value = salt_data[0]
            hashed_password_input = hash_password(password, salt_value)

            mycursor.execute("SELECT * FROM information WHERE email = %s AND password = %s", (email, hashed_password_input))
            user_data = mycursor.fetchone()

            if user_data:
                session['email'] = email
                return redirect(url_for('dashboard'))
            else:
                error_message = "Incorrect password. Please try again."

    return render_template('login.html', error_message=error_message)

@app.route('/new_acc', methods=['GET', 'POST'])
# Creates an account and stores the users informations securly to the data base while via salted password.
def new_acc():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = pass_check(request) 

        mycursor.execute("SELECT * FROM information WHERE email = %s", (email,))
        existing_user = mycursor.fetchone()

        if existing_user:
            return "An account with this email already exists. Please use a different email."

        if pass_length(password) and pass_capital(password) and pass_special(password) and pass_numerical(password):
            salt = generate_salt()
            hashed_password = hash_password(password, salt)
            mycursor.execute(sqlFormula, (username, email, hashed_password, salt, 0))
            mydb.commit()
            session['email'] = email
            return redirect(url_for('dashboard')) 
        else:
            return "Please enter a valid password that includes the following:\n- Capital letter\n- Special Character\n- 6 Characters\n- Numerical Value"

    return render_template('new_acc.html')

@app.route('/withdraw', methods=['GET', 'POST'])
# Sorts data base and withdraws amount from users email address as an id. If amount in account is less than withdraw, error message displays, else subtracts request from stored. 
# Tracks the transaction type along with amount to be later disaplyed on the dashboard screen a log of transactions. 
def withdraw():
    if 'email' in session:
        email = session['email']

        if request.method == 'POST':
            withdraw_amount = int(request.form.get('amount'))

            if withdraw_amount <= 0:
                return "Invalid withdrawal amount. Please enter a positive value."

            current_balance = get_balance(email)

            if withdraw_amount > current_balance:
                return "Insufficient funds. Withdrawal canceled."

            mycursor.execute("UPDATE information SET balance = balance - %s WHERE email = %s", (withdraw_amount, email))
            mydb.commit()

            mycursor.execute("INSERT INTO transactions (user_email, transaction_type, amount) VALUES (%s, %s, %s)", (email, 'Withdraw', withdraw_amount))
            mydb.commit()

            remaining_balance = get_balance(email)

            return redirect(url_for('withdraw', message="Withdrawal successful!", remaining_balance=remaining_balance))

        return render_template('withdraw.html')
    else:
        return redirect(url_for('login'))

@app.route('/deposit', methods=['GET', 'POST'])
# Sorts data and adds funds to the user by identifiying their email address in the database. If an invalid number is displayed it will handle error accordingly. 
# Tracks the transaction type along with amount to be later disaplyed on the dashboard screen a log of transactions. 
def deposit():
    if 'email' in session:
        email = session['email']

        if request.method == 'POST':
            deposit_amount = int(request.form.get('amount'))

            if deposit_amount <= 0:
                return "Invalid deposit amount. Please enter a positive value."

            mycursor.execute("UPDATE information SET balance = balance + %s WHERE email = %s", (deposit_amount, email))
            mydb.commit()

            mycursor.execute("INSERT INTO transactions (user_email, transaction_type, amount) VALUES (%s, %s, %s)", (email, 'Deposit', deposit_amount))
            mydb.commit()

            remaining_balance = get_balance(email)

            return redirect(url_for('deposit', message="Deposit successful!", remaining_balance=remaining_balance))

        return  render_template('deposit.html')
    else:
        return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
# Allows user to choose their transaction method. This also keeps an updated display of users balance on screen. Error handling for invalid request or inputs. 
def dashboard():
    if 'email' in session:
        email = session['email']

        if request.method == 'POST':
            action = request.form.get('action')

            if action == "deposit":
                deposit_amount = int(request.form.get('amount'))
                mycursor.execute("UPDATE information SET balance = balance + %s WHERE email = %s", (deposit_amount, email))
                mydb.commit()
                return f"Deposit successful! Remaining balance: ${get_balance(email)}"

            elif action == "withdraw":
                withdraw_amount = int(request.form.get('amount'))
                current_balance = get_balance(email)

                if withdraw_amount > current_balance:
                    return "Insufficient funds. Withdrawal canceled."
                else:
                    mycursor.execute("UPDATE information SET balance = balance - %s WHERE email = %s", (withdraw_amount, email))
                    mydb.commit()
                    return "Withdrawal successful!"

            elif action == "check_balance":
                return f"Current balance: ${get_balance(email)}"

            elif action == "wire_transfer":
                return redirect(url_for('wire_transfer'))

            else:
                return "Invalid action. Please choose a valid operation."

        username = get_username(email)
        current_balance = get_balance(email)

        mycursor.execute("SELECT * FROM transactions WHERE user_email = %s ORDER BY timestamp DESC LIMIT 5", (email,))
        transactions = mycursor.fetchall()
        transactions = [{'transaction_type': row[3], 'amount': row[2], 'timestamp': row[4]} for row in transactions]

        return render_template('dashboard.html', username=username, current_balance=current_balance, transactions=transactions)
    else:
        return redirect(url_for('login'))
        
@app.route('/wire_transfer', methods=['GET', 'POST'])
# Sorts data for senders email and withdraws money from the users account. Sender is prompted to enter the recipients email which will be used to send the withdrawn money to.
# Tracks the transaction type along with amount to be later disaplyed on the dashboard screen a log of transactions. 
def wire_transfer():
    if 'email' in session:
        email = session['email']

        if request.method == 'POST':
            recipient = request.form.get('recipient')
            wire_amount = int(request.form.get('amount'))

            recipient_exists = check_user_exists(recipient)

            if not recipient_exists:
                return "Recipient not found. Wire transfer canceled."

            current_balance = get_balance(email)

            if wire_amount > current_balance:
                return "Insufficient funds. Wire transfer canceled."

            mycursor.execute("UPDATE information SET balance = balance - %s WHERE email = %s", (wire_amount, email))
            mycursor.execute("UPDATE information SET balance = balance + %s WHERE email = %s", (wire_amount, recipient))
            mydb.commit()

            mycursor.execute("INSERT INTO transactions (user_email, transaction_type, amount) VALUES (%s, %s, %s)", (email, 'Wire Transfer', wire_amount))
            mydb.commit()

            remaining_balance = get_balance(email)
            return redirect(url_for('wire_transfer', message="Wire transfer successful!", remaining_balance=remaining_balance))

        return render_template('wire_transfer.html')
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)

# Close database connection on application exit
@app.teardown_appcontext
def close_db_connection(exception=None):
    mycursor.close()
    mydb.close()
