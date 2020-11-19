import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User, Form
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend homepage.

The tests will only test the frontend portion of the program, by patching the backend to return
specfic values. For example:

@patch('qa327.backend.get_user', return_value=test_user)

Will patch the backend get_user function (within the scope of the current test case)
so that it return 'test_user' instance below rather than reading
the user from the database.

Annotate @patch before unit tests can mock backend methods (for that testing function)
"""

# Mock a sample user
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('Test_frontend@'),
    balance=500
)

# Mock some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100', 'quantity': '2', 'email': 'test123@email.com', 'date': '02/23/2020'}
]

# Mock a sample buy form
test_sell_form = Form(
    name='buy_tix',
    quantity='2',
    price='50',
    date='02/23/2020'
)

class FrontEndHomePageTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_success(self, *_):
        """
        This is a sample front end unit test to login to home page
        and verify if the tickets are correctly listed. It also
        checks that the name, price, quantity, email and date are all listed
        """
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        
        # after clicking on the browser (the line above)
        # the front-end code is activated 
        # and tries to call get_user function.
        # The get_user function is supposed to read data from database
        # and return the value. However, here we only want to test the
        # front-end, without running the backend logics. 
        # so we patch the backend to return a specific user instance, 
        # rather than running that program. (see @ annotations above)
        
        
        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Hi test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100 2 test123@email.com 02/23/2020", "#tickets div h4")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_password_failed(self, *_):
        """ Login and verify if the tickets are correctly listed."""
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "wrong_password")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Incorrect Password", "#message")

    def test_not_loggedin(self, *_):
        """If the user hasnt logged in, show the login page"""
        #Open the logout page to invalidate any logged-in session
        self.open(base_url + '/logout')
        #open the login page
        self.open(base_url + '/login')
        #make sure it shows the proper page and message
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_show_header(self, *_):
        """Validate that this page shows a header ‘Hi {}’.format(user.name)"""
        # Open the logout page to invalidate any logged-in session
        self.open(base_url + '/logout')
        # open the login page
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # This page shows a header ‘Hi {}’.format(user.name)
        self.assert_element("#welcome-header")
        self.assert_text("Hi test_frontend", "#welcome-header")

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_balance(self, *_):
        """Validate that this page shows user balance"""
        # Open the logout page to invalidate any logged-in session
        self.open(base_url + '/logout')
        # open the login page
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        self.assert_element("#user-balance")
        self.assert_text("Your current balance is: 500", "#user-balance")

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_show_logout(self, *_):
        """Validate that there is a logout link"""
        # Open the logout page to invalidate any logged-in session
        self.open(base_url + '/logout')
        # open the login page
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        self.assert_element("#logout-link")

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_sell_buy(self, *_):
        """Validate buy form and fields name, quantity, price, exp date exist"""
        # Open the logout page to invalidate any logged-in session
        self.open(base_url + '/logout')
        # open the login page
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        self.assert_element("#name_sell")
        self.assert_element("#quantity_sell")
        self.assert_element("#price_sell")
        self.assert_element("#exp_date_sell")

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_form_buy(self, *_):
        """Validate buy form and fields name, quantity, price, exp date exist"""
        # Open the logout page to invalidate any logged-in session
        self.open(base_url + '/logout')
        # open the login page
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        self.assert_element("#name_buy")
        self.assert_element("#quantity_buy")






