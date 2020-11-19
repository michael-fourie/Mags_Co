import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
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
        self.assert_text("Email/Password format is incorrect", "#message")

    def test_not_loggedin(self, *_):
        """If the user hasnt logged in, show the login page"""
        """R1.1"""
        #Open the logout page to invalidate any logged-in session
        self.open(base_url + '/logout')
        #open the login page
        self.open(base_url + '/login')
        #make sure it shows the proper page and message
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

    def test_login_message(self, *_):
        """The login page has that by deafult says 'please login"""
        """R1.2"""
        # Open the logout page to invalidate any logged-in session
        self.open(base_url + '/logout')
        # open the login page
        self.open(base_url + '/login')
        # make sure it shows the proper page and message
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_logged_in_redirect(self, *_):
        """If the user has logged in, redirect to the user profile page"""
        """R1.3"""
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

    def test_login_two_fields(self, *_):
        """The login page provides a login form which requests two fields: email and password"""
        """R1.4"""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        #Check they exist
        self.assert_element('#email')
        self.assert_element('#password')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_as_post(self, *_):
        """The login form can be submitted as a POST request to the current url"""
        """R1.5"""
        self.open(base_url + '/login')
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        #If post request worked, hompeage should have user info
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

    def test_email_password_empty(self, *_):
        """Email and password both cannot be empty"""
        """R1.6"""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.click('input[type="submit"]')
        self.assert_element("#message")
        #Login should have failed, should still read please log in
        self.assert_text("Please login", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_valid_email(self, *_):
        """Email has to follow addr-spec defined in RFC 5322"""
        """R1.7"""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        #enter wrong email
        self.type("#email", "invalidemail")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        self.assert_text("Email format is incorrect", "#message")
        # fill email and password, email is valid and follows guidlines,
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")

    def test_invalid_password(self, *_):
        """Password has to meet requried complexity"""
        """R1.8"""
        # logout user to invalidate any logged in user
        self.open(base_url + "/logout")
        self.open(base_url + '/login')
        # enter an invalid password
        self.type("#password", "invld")
        self.type("#email", "test_frontend@test.com")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Email/Password format is incorrect", "#message")


    def test_formatting_errors(self, *_):
        """For any formatting error, render the login page and show the message
        'email / password format is incorrect '
        R1.9"""
        #Logout user to invalidate any logged in user
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        #Input invalid user and password
        self.type("#email", "invalidemail")
        self.type("#password", "invalidpassword")

        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Email/Password format is incorrect", "#message")


    @patch('qa327.backend.get_user', return_value=test_user)
    def test_email_password_correct(self, *_):
        """If email / password are correct, redirect to /"""
        """R1.10"""
        self.open(base_url +'/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

    def test_email_password_incorrect(self, *_):
        """Otherwise, redirect /login and show message 'email/password
        combination incorrect"""
        """R1.11"""
        #Logut to invalidate any logged user
        self.open(base_url + "/logout")
        self.open(base_url + "/login")
        # fill invalid email and password
        self.type("#email", "test_frontend_invalid_test.com")
        self.type("#password", "invalid")
        #click enter button
        self.click('input[type="submit"]')
        #open the home page
        self.assert_element("#message")
        self.assert_text("Email/Password format is incorrect", "#message")


