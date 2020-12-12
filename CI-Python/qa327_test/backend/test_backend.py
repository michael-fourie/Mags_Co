import pytest
from seleniumbase import BaseCase
from qa327.models import db, User, Ticket
from qa327_test.conftest import base_url
from qa327.backend import login_user
from unittest.mock import patch
from werkzeug.security import generate_password_hash, check_password_hash


test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('Test_frontend@')
)

test_tickets = [
    Ticket(name='t1', price=100, quantity=2, email='test1@email.com', date='20200223'),
    Ticket(name='t2', price=110, quantity=10, email='test2@gmail.com', date='20200314')
 ]

class BackEndUserTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_login_user(self, *_):
        """    ---Output Partitioning---
        The possible Inputs for the get_user() function in backend.py

        Input 1: A valid user email that belongs to a registered user, a valid password belonging to a user
        Input 2: An invalid user email that does not belong to a user, a valid password belonging to a user
        Input 3: A valid user email that belongs to a registered user, an invalid password not belonging to a user
        Input 4: An invalid user email that does not belong to a user, an invalid passwrod not belonging to a user

        Expected Output for 1: A user object belonging to the users email and password
        Expected Output for 2: A none type object
        Expected Output for 3: A none type object
        Expected output for 4: A none type object
        """

        # Enter valide email and password. Should take the user to the profile page and welcome them.
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", "Test_frontend@")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_text("Hi test_frontend", "#welcome-header")

        # Enter an invalid email. and a valid password. Should not let the user login since the login_user()
        # function should return a None type object
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.type("#email", "Invalid Email")
        self.type("#password", "Test_frontend@")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_text("Please login", "#message")

        # Enter a valid email, and an invalid password. Should not let the user login since the login_user()
        # function should return a None type object
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", "wrong password")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_text("Please login", "#message")

        # Enter an invalid email, and an invalid password. Should not let the user login since the login_user()
        # function should return a None type object
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.type("#email", "Invalid Email")
        self.type("#password", "Invalid Password")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_text("Please login", "#message")



