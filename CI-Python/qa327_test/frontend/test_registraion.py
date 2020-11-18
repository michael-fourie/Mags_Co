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

# Mock a sample user
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('Test_frontend@1'),
    balance=0
)
#Mock a sample registration user
test_user_register = User(
    email='register@test.ca',
    name='name_register',
    password=generate_password_hash('name_registe@1r'),
    balance=5000
    )

# Mock some sample tickets
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

    # def test_not_loggedin(self, *_):
    #     """If the user hasnt logged in, show the login page"""
    #     #Open the logout page to invalidate any logged-in session
    #     self.open(base_url + '/logout')
    #     #open the login page
    #     self.open(base_url + '/login')
    #     #make sure it shows the proper page and message
    #     self.assert_element("#message")cd
    #     self.asset_text("")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_has_logged_in(self, *_):  # R2.1 R2.2 [GET]
        """If the user hasn't logged in, show the login page"""
        # Open the logout page to invalidate any logged-in session
        # log out any previous users
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@1")
        # click enter button
        self.click('input[type="submit"]')
        # open register page
        self.open(base_url + '/register')  # Here should redirect to home page somehow. or the register
        # if they didn't log in
        # make sure it shows the proper page and message
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")

    def test_register_page(self, *_):  # R2.3 [GET]
        ''' The registration page shows a registration from requesting email, username,
        password, password2 '''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # validate that proper page and message are showing (Just '' for register page)
        self.assert_element("#message")
        self.asset_text("")

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register(self, *_):  # R2.4 AND R2.5 [POST]
        '''The registration form can be submitted as a POST request to current URL'''
        '''Email, password, and password2 all have to satisfy the same required in R1'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "new_frontend@test.com")
        #enter name into element
        self.type("#name",'name register')
        # enter password1 into element
        self.type("#password", 'name_register@1')
        # enter password 2 into element
        self.type("#password2", 'name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        #validate user profile creation is successful
        #validate redirection to login
        self.assert_element("#message")
        self.asset_text("")

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register(self, *_):  # R2.6 and R2.9 [POST]
        '''Password and Password 2 have to be exactly the same'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "new_frontend@test.com")
        # enter name into element
        self.type("#name", 'name register')
        # enter password1 into element
        self.type("#password", 'rname_register@1')
        # enter password 2 into element
        self.type("#password2", 'name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for non matching passwords
        self.assert_element("#message")
        self.asset_text("#message", "The passwords do not match")

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register(self, *_):  # R2.7A and R2.9 [POST]
        '''User name has to be non-empty'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "new_frontend@test.com")
        # enter name into element
        self.type("#name", '')
        # enter password1 into element
        self.type("#password", 'name_register@1')
        # enter password 2 into element
        self.type("#password2", 'name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for empty name
        self.assert_element("#message")
        self.asset_text("#message", "Name length formatting error")

        @patch('qa327.backend.register_user', return_value=test_user_register)
        @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
        def test_register(self, *_):  # R2.7B and R2.9 [POST]
            '''User name has to be alphanumeric only'''
            # log out any previous users
            self.open(base_url + '/logout')
            # open register page
            self.open(base_url + '/register')
            # enter email into element
            self.type("#email", "new_frontend@test.com")
            # enter name into element
            self.type("#name", '***')
            # enter password1 into element
            self.type("#password", 'name_register@1')
            # enter password 2 into element
            self.type("#password2", 'name_register@1')
            # click enter button
            self.click('input[type="submit"]')
            # validate error message is shown for empty name
            self.assert_element("#message")
            self.asset_text("#message", "Name contains special characters")

        @patch('qa327.backend.register_user', return_value=test_user_register)
        @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
        def test_register(self, *_):  # R2.7C and R2.9 [POST]
            '''User name has spaces allowed only if it is not the first or the last character'''
            # log out any previous users
            self.open(base_url + '/logout')
            # open register page
            self.open(base_url + '/register')
            # enter email into element
            self.type("#email", "new_frontend@test.com")
            # enter name into element
            self.type("#name", 'name register ')
            # enter password1 into element
            self.type("#password", 'name_register@1')
            # enter password 2 into element
            self.type("#password2", 'name_register@1')
            # click enter button
            self.click('input[type="submit"]')
            # validate error message is shown for empty name
            self.assert_element("#message")
            self.asset_text("#message", "Spacing error in name")

        @patch('qa327.backend.register_user', return_value=test_user_register)
        @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
        def test_register(self, *_):  # R2.8A and R2.9 [POST]
            '''User name has to be longer than 2 characters'''
            # log out any previous users
            self.open(base_url + '/logout')
            # open register page
            self.open(base_url + '/register')
            # enter email into element
            self.type("#email", "new_frontend@test.com")
            # enter name into element
            self.type("#name", 'na')
            # enter password1 into element
            self.type("#password", 'name_register@1')
            # enter password 2 into element
            self.type("#password2", 'name_register@1')
            # click enter button
            self.click('input[type="submit"]')
            # validate error message is shown for empty name
            self.assert_element("#message")
            self.asset_text("#message", "Name length formatting error")

        @patch('qa327.backend.register_user', return_value=test_user_register)
        @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
        def test_register(self, *_):  # R2.8B and R2.9 [POST]
            '''User name has to be less than 20 characters'''
            # log out any previous users
            self.open(base_url + '/logout')
            # open register page
            self.open(base_url + '/register')
            # enter email into element
            self.type("#email", "new_frontend@test.com")
            # enter name into element
            self.type("#name", 'name register toolong')
            # enter password1 into element
            self.type("#password", 'name_register@1')
            # enter password 2 into element
            self.type("#password2", 'name_register@1')
            # click enter button
            self.click('input[type="submit"]')
            # validate error message is shown for empty name
            self.assert_element("#message")
            self.asset_text("#message", "Name length formatting error")

        @patch('qa327.backend.register_user', return_value=test_user_register)
        @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
        def test_register(self, *_):  # R2.8B and R2.9 [POST]
            '''For any formatting errors, redirect back to /login and show message '{}
            format is incorrect.'.format(the_corresponding_attribute)'''
            # log out any previous users
            self.open(base_url + '/logout')
            # open register page
            self.open(base_url + '/register')
            # enter email into element
            self.type("#email", "new_frontend@test.com")
            # enter name into element
            self.type("#name", 'name register toolong')
            # enter password1 into element
            self.type("#password", 'name_register@1')
            # enter password 2 into element
            self.type("#password2", 'name_register@1')
            # click enter button
            self.click('input[type="submit"]')
            # validate error message is shown for empty name
            self.assert_element("#message")
            self.asset_text("#message", "Name length formatting error")

        @patch('qa327.backend.register_user', return_value=test_user_register)
        @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
        def test_register(self, *_):  # R2.8B and R2.9 [POST]
            '''If the email already exists, show message 'this email has been ALREADY used'''
            # log out any previous users
            self.open(base_url + '/logout')
            # open register page
            self.open(base_url + '/register')
            # enter email into element
            self.type("#email", "test_frontend@test.com")  # email is same as test_user_register
            # enter name into element
            self.type("#name", 'name register toolong')
            # enter password1 into element
            self.type("#password", 'name_register@1')
            # enter password 2 into element
            self.type("#password2", 'name_register@1')
            # click enter button
            self.click('input[type="submit"]')
            # validate error message is shown for empty name
            self.assert_element("#message")
            self.asset_text("#message", "This email has already been used")

        @patch('qa327.backend.register_user', return_value=test_user_register)
        @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
        def test_register(self, *_):  # R2.8B and R2.9 [POST]
            '''If no error regarding the inputs following the rules above, create
            a new user, set the balance to 5000, and go back to the /login page'''
            # log out any previous users
            self.open(base_url + '/logout')
            # open register page
            self.open(base_url + '/register')
            # enter email into element
            self.type("#email", "new_frontend@test.com")
            # enter name into element
            self.type("#name", 'name register')
            # enter password1 into element
            self.type("#password", 'name_register@1')
            # enter password 2 into element
            self.type("#password2", 'name_register@1')
            # click enter button
            self.click('input[type="submit"]')
            # validate user profile creation is successful
            # validate redirection to login
            self.assert_element("#message")
            self.asset_text("")