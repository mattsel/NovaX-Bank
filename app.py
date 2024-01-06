from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
import random
from dotenv import load_dotenv
import os
from datetime import datetime

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

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

# Formula to insert information into database in a simplified manner for both transaction database and the credit applications. 
transactionFormula = "INSERT INTO transactions (user_email, transaction_type, amount) VALUES (%s, %s, %s)"
creditcardFormula = "INSERT INTO credit_applications (first_name, last_name, email, address, city, state, postal_code, annual_income) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

# Retrieve user balance from the database.
def get_balance(email):
    user = User.query.filter_by(email=email).first()
    return user.balance if user else None

# Retrieve username associated with the given email.
def get_username(email):
    user = User.query.filter_by(email=email).first()
    return user.username if user else None

# Check if a user with the given email exists in the database.
def check_user_exists(email):
    return User.query.filter_by(email=email).first() is not None

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
    
# Check eligibility based on annual income
def check_eligibility(annual_income):
    return annual_income >= 35000
    
@app.route('/')
def index():
    return render_template('index.html')

# Handle user login by checking if an account exists.
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    # Check if the request method is POST
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Retrieve user information based on the provided email
        user = User.query.filter_by(email=email).first()

        if user:
            # Retrieve salt and hash the input password for comparison
            salt_value = user.salt
            hashed_password_input = hash_password(password, salt_value)

            # Check if the hashed input password matches the stored password
            if user.password == hashed_password_input:
                # Set the user's email in the session and redirect to the dashboard
                session['email'] = email
                return redirect(url_for('dashboard'))
            else:
                # Display an error message for incorrect password
                error_message = "Incorrect password. Please try again."

    # Render the login template with the appropriate error message
    return render_template('login.html', error_message=error_message)

@app.route('/new_acc', methods=['GET', 'POST'])
def new_acc():
    # Check if the request method is POST
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = pass_check(request)

        # Check if a user with the same email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "An account with this email already exists. Please use a different email."

        # Validate the password based on specified criteria
        if (
            pass_length(password) and
            pass_capital(password) and
            pass_special(password) and
            pass_numerical(password)
        ):
            # Generate salt and hash the password
            salt = generate_salt()
            hashed_password = hash_password(password, salt)

            # Create and commit the new user to the database
            new_user = User(username=username, email=email, password=hashed_password, salt=salt, balance=0)
            db.session.add(new_user)
            db.session.commit()

            # Set the user's email in the session and redirect to the dashboard
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            # Return an error message if the password criteria are not met
            return "Please enter a valid password that includes the following:\n- Capital letter\n- Special Character\n- 6 Characters\n- Numerical Value"

    # Render the new account template for GET requests
    return render_template('new_acc.html')


@app.route('/credit', methods=['GET', 'POST'])
def credit():
    message = None

    # Check if the request method is POST
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        postal_code = request.form.get('postal_code')
        annual_income = request.form.get('annual_income')

        # Validate the annual income (must be a positive integer)
        if not annual_income.isdigit():
            flash("Please enter a valid annual income.", 'error')
        else:
            annual_income = int(annual_income)

            # Check eligibility based on annual income
            if check_eligibility(annual_income):
                # Check if an application with the same email already exists
                count = CreditApplication.query.filter_by(email=email).count()

                if count > 0:
                    flash("An application with this email already exists. Please use a different email.", 'error')
                else:
                    # Check if a user with the same email already exists
                    if check_user_exists(email):
                        flash("An account with this email already exists. Please use a different email.", 'error')
                    else:
                        # Create and commit the credit application to the database
                        credit_application = CreditApplication(
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            address=address,
                            city=city,
                            state=state,
                            postal_code=postal_code,
                            annual_income=annual_income
                        )
                        db.session.add(credit_application)
                        db.session.commit()
                        flash("Credit card application submitted!", 'success')
            else:
                flash("Income does not meet our criteria to be a NovaX Credit Card holder", 'error')

    # Render the credit template with the appropriate messages
    return render_template('credit.html')


@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    # Check if the user is logged in (session contains 'email')
    if 'email' in session:
        # Retrieve user information from the database based on the email in the session
        email = session['email']
        user = User.query.filter_by(email=email).first()

        # Check if the request method is POST
        if request.method == 'POST':
            # Get deposit amount from the form
            deposit_amount = int(request.form.get('amount'))

            # Validate the deposit amount
            if deposit_amount <= 0:
                flash("Invalid deposit amount. Please enter a positive value.", 'error')
            else:
                # Perform the deposit by updating the user's balance and recording the transaction
                user.balance += deposit_amount
                db.session.commit()
 
                transaction = Transaction(user_email=email, transaction_type='Deposit', amount=deposit_amount)
                db.session.add(transaction)
                db.session.commit()

                flash("Deposit successful!", 'success')

        # Get the remaining balance after deposit
        remaining_balance = user.balance

        # Render the deposit template with user information and remaining balance
        return render_template('deposit.html', user=user, remaining_balance=remaining_balance)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))
    
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    # Check if the user is logged in (session contains 'email')
    if 'email' in session:
        # Retrieve user information from the database based on the email in the session
        email = session['email']
        user = User.query.filter_by(email=email).first()

        # Check if the request method is POST
        if request.method == 'POST':
            # Get withdrawal amount from the form
            withdraw_amount = int(request.form.get('amount'))

            # Validate the withdrawal amount
            if withdraw_amount <= 0:
                flash("Invalid withdrawal amount. Please enter a positive value.", 'error')
            elif withdraw_amount > user.balance:
                flash("Insufficient funds. Withdrawal canceled.", 'error')
            else:
                # Perform the withdrawal by updating the user's balance and recording the transaction
                user.balance -= withdraw_amount
                db.session.commit()

                transaction = Transaction(user_email=email, transaction_type='Withdraw', amount=withdraw_amount)
                db.session.add(transaction)
                db.session.commit()

                flash("Withdrawal successful!", 'success')

        # Get the remaining balance after withdrawal
        remaining_balance = user.balance

        # Render the withdrawal template with user information and remaining balance
        return render_template('withdraw.html', user=user, remaining_balance=remaining_balance)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

@app.route('/wire_transfer', methods=['GET', 'POST'])
def wire_transfer():
    # Check if the user is logged in (session contains 'email')
    if 'email' in session:
        # Retrieve user information from the database based on the email in the session
        email = session['email']
        user = User.query.filter_by(email=email).first()

        # Check if the request method is POST
        if request.method == 'POST':
            # Get recipient and wire amount from the form
            recipient = request.form.get('recipient')
            wire_amount = int(request.form.get('amount'))

            # Check if the recipient exists in the system
            recipient_exists = check_user_exists(recipient)

            if not recipient_exists:
                flash("Recipient not found. Wire transfer canceled.", 'error')
            else:
                # Check if the user has sufficient funds for the wire transfer
                current_balance = user.balance

                if wire_amount > current_balance:
                    flash("Insufficient funds. Wire transfer canceled.", 'error')
                else:
                    # Perform the wire transfer by updating balances and recording the transaction
                    user.balance -= wire_amount
                    recipient_user = User.query.filter_by(email=recipient).first()
                    recipient_user.balance += wire_amount
                    db.session.commit()

                    # Record the wire transfer transaction in the database
                    transaction = Transaction(user_email=email, transaction_type='Wire Transfer', amount=wire_amount)
                    db.session.add(transaction)
                    db.session.commit()

                    flash("Wire transfer successful!", 'success')

        # Get the remaining balance after wire transfer
        remaining_balance = user.balance

        # Render the wire transfer template with user information and remaining balance
        return render_template('wire_transfer.html', user=user, remaining_balance=remaining_balance)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Check if the user is logged in (session contains 'email')
    if 'email' in session:
        # Retrieve user information from the database based on the email in the session
        email = session['email']
        user = User.query.filter_by(email=email).first()

        # Check if the request method is POST
        if request.method == 'POST':
            # Get the action parameter from the form
            action = request.form.get('action')

            # Deposit funds if the action is 'deposit'
            if action == "deposit":
                deposit_amount = int(request.form.get('amount'))
                user.balance += deposit_amount
                db.session.commit()

                # Record the deposit transaction in the database
                transaction = Transaction(user_email=email, transaction_type='Deposit', amount=deposit_amount)
                db.session.add(transaction)
                db.session.commit()

                flash("Deposit successful!", 'success')

            # Withdraw funds if the action is 'withdraw'
            elif action == "withdraw":
                withdraw_amount = int(request.form.get('amount'))
                current_balance = user.balance

                # Check if there are sufficient funds for withdrawal
                if withdraw_amount > current_balance:
                    flash("Insufficient funds. Withdrawal canceled.", 'error')
                else:
                    # Update the user's balance and record the withdrawal transaction
                    user.balance -= withdraw_amount
                    db.session.commit()

                    transaction = Transaction(user_email=email, transaction_type='Withdraw', amount=withdraw_amount)
                    db.session.add(transaction)
                    db.session.commit()

                    flash("Withdrawal successful!", 'success')

        # Retrieve the latest 5 transactions for the user
        transactions = Transaction.query.filter_by(user_email=email).order_by(Transaction.timestamp.desc()).limit(5).all()

        # Render the dashboard template with user information and recent transactions
        return render_template('dashboard.html', user=user, username=user.username, current_balance=user.balance, transactions=transactions)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

def create_tables():
    with app.app_context():
        db.create_all() 

if __name__ == "__main__":
    create_tables()
    app.run(debug=True) 


# Close the database connection on application exit
@app.teardown_appcontext
def close_db_connection(exception=None):
    db.session.remove()