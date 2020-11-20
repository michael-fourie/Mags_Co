import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User,Form
from werkzeug.security import generate_password_hash, check_password_hash
import requests

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

# Moch a sample user
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('Test_frontend@')
)

# Moch some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100'}
]



class FrontEndHomePageTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_success(self, *_):
        """
        This is a sample front end unit test to login to home page
        and verify if the tickets are correctly listed.
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
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

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

    # Check to see that when a user's credentials are entered into the
    # /register, when they click the input[type=”submit”] their form is submitted.
    # test case R2.4
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_registration_form(self, *_):
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')

        # enter correct user and password
        self.type('#email', 'test_frontend@test.com')
        self.type('#name', 'test_frontend')
        self.type('#password', 'test_frontend')
        self.type('#password2', 'test_frontend')
        # click submit button to submit form
        self.click('input[type="submit"]')

        # redirect back to login page
        self.open(base_url + '/login')

        # verify correct header is displayed
        self.assert_element('#message')
        #self.assert_text("")

        # Ensure that the login page is showing after the user submits logout. Ensure that none of
        # the pages can be accessed if user tries to type in their address.
        # test case R7.1

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_logout(self, *_):
        self.open(base_url + '/logout')
        self.open(base_url + '/')

        #returns true if correct message is displayed
        self.assert_element('#message')

        # Check that when anything after the backslash that has not been defined (/*) returns a 404 error code.
        # test case R8.1

    def test_unexpected_input(self):
        self.open(base_url + '/*')
        self.open(base_url)

        #retrieves status code of action
        r = requests.get(base_url + '/*')

        #returns true if correct error message is displayed (404 not found)
        assert (r.status_code == 404)


        # Validate that the ticket-update form can be posted to /update
        # test case R3.10

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_ticket_update_form(self, *_):
        # log out any previous users
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')

        self.open(base_url)

        self.click('input[type="submit"]')
        self.open(base_url + '/update')

        # Validate that the ticket-buying form can be posted to /buy
        #test case R3.9

    @patch('qa327.backend.get_user', return_value=test_user)

    def test_ticket_buy_form(self, *_):
        # log out any previous users
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')

        self.open(base_url)


        #fills out buy form
        self.type('#name_buy', 'new_ticket')
        self.type('#quantity_buy', '10')

        self.click('input[id="submit_buy"]')

        #returns true if form_buy was POSTed
        self.assert_element('#form_buy')

    # Validate that the ticket-selling form can be posted to /sell
    # test case for R3.8
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_ticket_sell_form(self, *_):
        # log out any previous users
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')

        self.open(base_url)

        #fills out sell form
        self.type('#name_sell', 'new_sell_ticket')
        self.type('#quantity_sell', '10')
        self.type('#price_sell', '10')
        self.type('#exp_date_sell', '20201031')

        #submits sell form
        self.click('input[id="submit_sell"]')

        self.open(base_url)
        #verifies form_sell was POSTed to /
        self.assert_element("#form_sell")


