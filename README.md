# NovaX Bank
**TEST THIS PROGRAM HERE:** [www.novax.mattsel.com](https://www.novax.mattsel.com)

**Overview:** The goal of this project was to exercise my skills in a full stack CRUD API banking application. In this project most of the styling was done with majority HTML, CSS, and slight JS for animations. The majority of the backend logic was done using Python and Flask while the database is configured with PostgreSQL. Throughout this project some of the key features in this app is that it includes login authentication, password salting, dynamic routing, and the ability to display user's transaction history logs via the dashboard. 

**Languages:** Python, PostgreSQL, HTML, CSS, JS, and Flask framework

**Libraries:** Unittest, Hashlib, Flask_Sqlalchemy, Dotenv, Flask, 

**Database:** PostgreSQL is used to store data in three separate tables: User, CreditApplication, and Transactions. Each of these tables stores the information that is provided by the user from forms and other inputs throughout the site i.e. deposits, withdraws, and transfers. 

![Screenshot 2024-01-06 201324](https://github.com/mattsel/NovaX-Bank/assets/141775337/a4073228-6ef1-453e-bd36-fd9af7b9e18a)

**Unit Testing:** An example of the unit testing done to ensure the database functions work properly is by inserting a new user and asserting that the database contains the newly added attributes.

<img width="563" alt="Screenshot 2024-01-07 at 12 15 52 PM" src="https://github.com/mattsel/NovaX-Bank/assets/141775337/09e118e7-99d9-4daa-80e8-4b2681c665c7">

**Database Info Formula:** The information entered into the tables is done using a formula that will be called at the end of the function to store the proper values for each of the columns. 

![Screenshot 2024-01-06 201502](https://github.com/mattsel/NovaX-Bank/assets/141775337/2358fb60-e668-47f4-b89e-25a36cb5c6d2)

**Password Complexity:** To ensure users have a secure password, many tests are done to check for complexity in the user's input i.e. length, numerical, special characters, and capitalization.

![Screenshot 2024-01-06 201718](https://github.com/mattsel/NovaX-Bank/assets/141775337/a5b9fbd5-b628-4a82-b9d9-3c08bbf556e0)

**Salting/Hashing:** After the user's password is ensured to have minimal complexity, before storing it in the database, it must first be salted in case of a cyber attack. This ensures the user's private information is kept secure from unauthorized access.

![Screenshot 2024-01-06 201851](https://github.com/mattsel/NovaX-Bank/assets/141775337/23add48a-be86-4b94-9c93-d7e6da53b3fa)

**User Authentication:** If the user has a pre-existing account, they will be prompted with a form to enter their email and password. The system will then check the database for the matching email and salted password using that user's stored salt. If the information matches, it will grant access, else print an error message. 

![Screenshot 2024-01-06 202221](https://github.com/mattsel/NovaX-Bank/assets/141775337/546fb184-152a-4a84-a37c-6457b72aa8c2)

**New Accounts:** If the user does not have an account they can create a new account similarly with a form to enter their information to create an account, which will be stored in the database to be later checked for when logging back in. 

![Screenshot 2024-01-06 202520](https://github.com/mattsel/NovaX-Bank/assets/141775337/d039404f-5222-49de-89b0-92942c8fd2e5)

**Credit Service:** The user can also choose to not create an account or log in, but they can still sign up for the NovaX Credit Card. This card is presented with a 3d model of the card and a short description along with a form to sign up. The user information entered will be stored in the credit application table for a duplicate application that was created. The threshold for the NovaX Card is that the user must report an income over $35,0000, or else it will show an error message that their income is too low. 

![Screenshot 2024-01-06 202823](https://github.com/mattsel/NovaX-Bank/assets/141775337/51f48154-94ac-4b62-a626-8d0519d84ec0)

**Dashboard Transaction Log:** After the user logs in or creates an account they will then be prompted to the dashboard screen which will greet the user based on their username and display their current balance. On the right side of the screen, they can choose to either make a deposit, withdraw, or wire transfer to other users by entering their email. On the bottom left of the screen, there is the user's transaction history by fetching their previous transactions from the transactions table.

![Screenshot 2024-01-06 202936](https://github.com/mattsel/NovaX-Bank/assets/141775337/2ffb2221-6d64-4256-81f8-ab0219eee848)

**Deposit/Withdraw:** The deposit and withdrawal are done similarly by first sorting through the database for the user's email address. Then based on the transaction type, it will perform the following actions for a deposit, add the amount requested to their balance, or for withdrawal, subtract that amount. Something to note is the error handling involved in the withdraw function. If a user withdraws more than their current account balance, it will decline the transaction and prompt an error message. 

![Screenshot 2024-01-06 203522](https://github.com/mattsel/NovaX-Bank/assets/141775337/19b14a2d-d6af-4f1d-ae1c-b737fc8af3bd)

**Wire Transfer:** The final action that the user can choose from, is a wire transfer by entering the recipient's email and amount they would like to send. Much like the withdraw function, it sorts through the database to find the user's email. Based on their email, it will then check that the amount of money they have in their account is not lower than the amount they are trying to send. If the user is sending an appropriate amount of money, it will then search the database for the recipient's email and add the amount selected to their account while subtracting that same amount from the sender's account. 

![Screenshot 2024-01-06 203914](https://github.com/mattsel/NovaX-Bank/assets/141775337/0fbcb361-ada6-4b32-885b-60d7bd4fe1fb)

**Database Query:** The following are the functions that are called to search through the database for the user's email and perform the following actions. 

![Screenshot 2024-01-06 203954](https://github.com/mattsel/NovaX-Bank/assets/141775337/1fc82093-1458-4c56-b4ab-df729dd7f1d6)

**Thank you for checking out NovaX Banking**
