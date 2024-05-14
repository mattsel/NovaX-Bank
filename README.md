# NovaX Bank
**TEST THIS PROGRAM HERE:** [www.novax.mattsel.com](https://www.novax.mattsel.com)

**Overview:** The goal of this project was to exercise my skills in a full-stack CRUD API banking application. In this project, most of the styling was done with the majority of HTML, CSS, and JS for animations. The majority of the backend logic was done using Python and Flask while the database is configured with PostgreSQL. Throughout this project, some of the key features in this app is that it includes login authentication, password salting, dynamic routing, and the ability to display user's transaction history logs via the dashboard. This application is also deployed to a cloud-based service, Render, to practice my ability to work with cloud services and gain more experience in the realm of deploying applications. 

**Languages:** Python, PostgreSQL, HTML, CSS, JS, and Flask framework

**Libraries:** Unittest, Hashlib, Flask_Sqlalchemy, Dotenv, Flask, 

**Database:** PostgreSQL is used to store data in three separate tables: User, CreditApplication, and Transactions. Each of these tables stores the information that is provided by the user from forms and other inputs throughout the site i.e. deposits, withdraws, and transfers. 

```python 
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
```
    
**Unit Testing:** An example of the unit testing done to ensure the database functions work properly is by inserting a new user and asserting that the database contains the newly added attributes.

```python
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
```

**Database Info Formula:** The information entered into the tables is done using a formula that will be called at the end of the function to store the proper values for each of the columns. 

```python
# Formula to insert information into database in a simplified manner for both transaction database and the credit applications. 
transactionFormula = "INSERT INTO transactions (user_email, transaction_type, amount) VALUES (%s, %s, %s)"
creditcardFormula = "INSERT INTO credit_applications (first_name, last_name, email, address, city, state, postal_code, annual_income) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
```

**Password Complexity:** To ensure users have a secure password, many tests are done to check for complexity in the user's input i.e. length, numerical, special characters, and capitalization.

```python
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
```

**Salting/Hashing:** After the user's password is ensured to have minimal complexity, before storing it in the database, it must first be salted in case of a cyber attack. This ensures the user's private information is kept secure from unauthorized access.

```python
# Generate a random salt for password hashing.
def generate_salt():
    return str(random.randint(100000, 999999))

# Hash the password using SHA-256 algorithm and the provided salt.
def hash_password(password, salt):
    hashed_password = hashlib.sha256((password + str(salt)).encode()).hexdigest()
    return hashed_password
```

**User Authentication:** If the user has a pre-existing account, they will be prompted with a form to enter their email and password. The system will then check the database for the matching email and salted password using that user's stored salt. If the information matches, it will grant access, else print an error message. 

```python
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
                 flash("Incorrect password. Please try again.", 'error')

    # Render the login template with the appropriate error message
    return render_template('login.html')
```

**New Accounts:** If the user does not have an account they can create a new account similarly with a form to enter their information to create an account, which will be stored in the database to be later checked for when logging back in. 

```python
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
           flash("An application with this email already exists. Please use a different email.", 'error')

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
            flash("Please ensure your password matches and includes the following: 6 Characters, Captial, Special Character, and Numerical Value ", 'error')

    # Render the new account template for GET requests
    return render_template('new_acc.html')
```

**Credit Service:** The user can also choose to not create an account or log in, but they can still sign up for the NovaX Credit Card. This card is presented with a 3d model of the card and a short description along with a form to sign up. The user information entered will be stored in the credit application table for a duplicate application that was created. The threshold for the NovaX Card is that the user must report an income over $35,0000, or else it will show an error message that their income is too low. 

```python
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
```

**Dashboard Transaction Log:** After the user logs in or creates an account they will then be prompted to the dashboard screen which will greet the user based on their username and display their current balance. On the right side of the screen, they can choose to either make a deposit, withdraw, or wire transfer to other users by entering their email. On the bottom left of the screen, there is the user's transaction history by fetching their previous transactions from the transactions table.

```python
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
        transactions = Transaction.query.filter_by(user_email=email).order_by(Transaction.timestamp.desc()).limit(10).all()

        # Render the dashboard template with user information and recent transactions
        return render_template('dashboard.html', user=user, username=user.username, current_balance=user.balance, transactions=transactions)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))
```

**Deposit/Withdraw:** The deposit and withdrawal are done similarly by first sorting through the database for the user's email address. Then based on the transaction type, it will perform the following actions for a deposit, add the amount requested to their balance, or for withdrawal, subtract that amount. Something to note is the error handling involved in the withdraw function. If a user withdraws more than their current account balance, it will decline the transaction and prompt an error message. 

```python

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
            deposit_amount = float(request.form.get('amount'))


            # Validate the deposit amount
            if deposit_amount <= 0:
                flash("Invalid deposit amount. Please enter a positive value.", 'error')
            else:
                # Perform the deposit by updating the user's balance and recording the transaction
                user.balance = round(user.balance + deposit_amount, 2)
                db.session.commit()
 
                transaction = Transaction(user_email=email, transaction_type='Deposit', amount=deposit_amount)
                db.session.add(transaction)
                db.session.commit()

                flash("Deposit successful!", 'success')

        # Get the remaining balance after deposit
        remaining_balance = round(user.balance, 2)

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
            withdraw_amount = float((request.form.get('amount')))

            # Validate the withdrawal amount
            if withdraw_amount <= 0:
                flash("Invalid withdrawal amount. Please enter a positive value.", 'error')
            elif withdraw_amount > user.balance:
                flash("Insufficient funds. Withdrawal canceled.", 'error')
            else:
                # Perform the withdrawal by updating the user's balance and recording the transaction
                user.balance = round(user.balance - withdraw_amount, 2)
                db.session.commit()

                transaction = Transaction(user_email=email, transaction_type='Withdraw', amount=withdraw_amount)
                db.session.add(transaction)
                db.session.commit()

                flash("Withdrawal successful!", 'success')

        # Get the remaining balance after withdrawal
        remaining_balance = round(user.balance, 2)

        # Render the withdrawal template with user information and remaining balance
        return render_template('withdraw.html', user=user, remaining_balance=remaining_balance)
    else:
        # Redirect to the login page if the user
```

**Wire Transfer:** The final action that the user can choose from, is a wire transfer by entering the recipient's email and amount they would like to send. Much like the withdraw function, it sorts through the database to find the user's email. Based on their email, it will then check that the amount of money they have in their account is not lower than the amount they are trying to send. If the user is sending an appropriate amount of money, it will then search the database for the recipient's email and add the amount selected to their account while subtracting that same amount from the sender's account. 

```python
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
            wire_amount = round(float((request.form.get('amount'))),2)

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
                    user.balance = round(user.balance - wire_amount, 2)
                    recipient_user = User.query.filter_by(email=recipient).first()
                    recipient_user.balance = round(recipient_user.balance + wire_amount, 2)
                    db.session.commit()

                    # Record the wire transfer transaction in the database
                    transaction = Transaction(user_email=email, transaction_type='Wire Transfer', amount=wire_amount)
                    db.session.add(transaction)
                    db.session.commit()

                    flash("Wire transfer successful!", 'success')

        # Get the remaining balance after wire transfer
        remaining_balance = round(user.balance, 2)

        # Render the wire transfer template with user information and remaining balance
        return render_template('wire_transfer.html', user=user, remaining_balance=remaining_balance)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))
```

**Database Query:** The following are the functions that are called to search through the database for the user's email and perform the following actions. 

```python
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
```

**Thank you for checking out NovaX Banking**
