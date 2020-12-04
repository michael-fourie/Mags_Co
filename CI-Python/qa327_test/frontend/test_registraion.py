import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User, Form

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

# Mock a sample user
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('Test_frontend@'),
    balance=500

)
# Mock a sample registration user
test_user_register = User(
    email='register@test.ca',
    name='nameregister',
    password=generate_password_hash('Name_register@1'),
    balance=5000
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
        self.assert_text("Email/Password format is incorrect", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_has_logged_in(self, *_):  # R2.1 R2.2 [GET]
        """If the user has logged in, redirect back to the user profile page"""
        # Open the logout page to invalidate any logged-in session
        # log out any previous users
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open base home page
        self.open(base_url)
        #  make sure it shows the proper page and message
        self.assert_element("#welcome-header")
        self.assert_text("Hi test_frontend", "#welcome-header")

    @patch('qa327.backend.register_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_hasnt_logged_in(self, *_):
        '''If the user hasn't logged in, show the user registration page'''
        # R2.2
        # Open the logout page to invalidate any logged-in session
        # log out any previous users
        self.open(base_url + '/logout')
        # open the registration
        self.open(base_url + '/register')
        # make sure proper page and message is showing
        self.assert_element("#message")
        self.assert_text("Register", "#message")

    @patch('qa327.backend.register_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_page(self, *_):  # R2.3 [GET]
        ''' The registration page shows a registration from requesting email, username,
        password, password2 '''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # validate that proper page and message are showing and can enter in the following:
        # enter email into element
        self.type("#email", "new_frontend@test.com")
        # enter name into element
        self.type("#name",'name register')
        # enter password1 into element
        self.type("#password", 'Name_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # assert register message element is showing
        self.assert_element("#message")
        self.assert_text("Register", "#message")

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
        # enter name into element
        self.type("#name",'name register')
        # enter password1 into element
        self.type("#password", 'Name_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # send to login page
        self.open(base_url + '/login')
        # validate user profile creation is successful
        # validate redirection to login
        self.assert_element("#message")

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_non_match(self, *_):  # R2.6 and R2.9 [POST]
        '''Password and Password 2 have to be exactly the same'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "new_frontend@test.com")
        # enter name into element
        self.type("#name", 'nameregister')
        # enter password1 into element
        self.type("#password", 'rName_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for non matching passwords
        self.assert_element("#message")
        self.assert_text("The passwords do not match", "#message")

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_empty(self, *_):  # R2.7A and R2.9 [POST]
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
        self.type("#password", 'Name_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for empty name
        self.assert_element("#message")
        self.assert_text("Register", "#message")
        # assert message still says register

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_alnum(self, *_):  # R2.7B and R2.9 [POST]
        '''User name has to be alphanumeric only'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "register@test.ca")             
        # enter name into element                                  
        self.type("#name", '$invalid_name$')                        
        # enter password1 into element
        self.type("#password", 'Name_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for special chars
        self.assert_element("#message")
        self.assert_text("Name contains special characters", "#message")

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_space(self, *_):  # R2.7C and R2.9 [POST]
        '''User name has spaces allowed only if it is not the first or the last character'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "new_frontend@test.com")                    
        # enter name into element                                       
        self.type("#name", 'nameregister ')
        # enter password1 into element
        self.type("#password", 'Name_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for spacing error in name
        self.assert_element("#message")
        self.assert_text("Invalid spaces found in word", "#message")

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_name_short(self, *_):  # R2.8A and R2.9 [POST]
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
        self.type("#password", 'Name_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for length error in name
        self.assert_element("#message")
        self.assert_text("Name length formatting error", "#message")

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_name_long(self, *_):  # R2.8B and R2.9 [POST]
        '''User name has to be less than 20 characters'''
        # log out any previous users
        self.open(base_url + '/logout')                                 
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "new_frontend@test.com")
        # enter name into element
        self.type("#name", 'nameregistertoolonggggg')
        # enter password1 into element
        self.type("#password", 'Name_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for length error in name
        self.assert_element("#message")
        self.assert_text("Name length formatting error", "#message")

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_email_short(self, *_):  # R2.8B and R2.9 [POST]
        '''Email has to be longer than 1 character'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "a")
        # enter name into element
        self.type("#name", 'nameregister')
        # enter password1 into element
        self.type("#password", 'Name_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for length error in name
        self.assert_element("#message")
        self.assert_text("Email format is incorrect", "#message")


    @patch('qa327.backend.get_user', return_value=None)
    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_format_email(self, *_):  # R2.8B and R2.9 [POST]
        '''For any formatting errors, redirect back to /login and show message '{}
        format is incorrect.'.format(the_corresponding_attribute)
        For email formatting errors'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')                               
        # enter email into element
        self.type("#email", "invalidemail")
        # enter name into element
        self.type("#name", 'nameregister')
        # enter password1 into element
        self.type("#password", 'Name_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for formatting error in name
        self.assert_element("#message")
        self.assert_text("Email format is incorrect", "#message")

    @patch('qa327.backend.get_user', return_value=None)
    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_format_password(self, *_):  # R2.8B and R2.9 [POST]
        '''For any formatting errors, redirect back to /login and show message '{}
        format is incorrect.'.format(the_corresponding_attribute)
        For password formatting errors.'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "register@test.ca")
        # enter name into element
        self.type("#name", 'nameregister')
        # enter password1 into element
        self.type("#password", 'invalidpass')
        # enter password 2 into element
        self.type("#password2", 'invalidpass')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for formatting error in name
        self.assert_element("#message")
        self.assert_text("Password format is incorrect", "#message")


    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_register_email_already_used(self, *_):  # R2.8B and R2.9 [POST]
        '''If the email already exists, show message 'this email has been ALREADY used'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "register@test.ca")  # email is same as test_user_register
        # enter name into element
        self.type("#name", 'nameregister')                    
        # enter password1 into element                          
        self.type("#password", 'Name_register@1')              
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')
        # click enter button
        self.click('input[type="submit"]')
        # validate error message is shown for email already used
        self.assert_element("#message")
        self.assert_text("This email has already been used", "#message")

    @patch('qa327.backend.register_user', return_value=test_user_register)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_user', return_value=None)
    def test_register_success(self, *_):  # R2.8B and R2.9 [POST]
        '''If no error regarding the inputs following the rules above, create
        a new user, set the balance to 5000, and go back to the /login page'''
        # log out any previous users
        self.open(base_url + '/logout')
        # open register page
        self.open(base_url + '/register')
        # enter email into element
        self.type("#email", "register@test.com")
        # enter name into element
        self.type("#name", 'nameregister')
        # enter password1 into element
        self.type("#password", 'Name_register@1')
        # enter password 2 into element
        self.type("#password2", 'Name_register@1')                    
        # click enter button
        self.click('input[type="submit"]')
        # validate user profile creation is successful
        # validate register successful
        self.assert_element("#message")
        # now go to the login page
        self.open(base_url + '/login')
        # validate user profile creation is successful
        # validate redirection to login
        self.assert_element("#message")
        self.assert_text("Please login", "#message")
        
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_show_header(self, *_):
        """Validate that this page shows a header ‘Hi {}’.format(user.name)"""
        """R3.2"""
        # Open the logout page to invalidate any logged-in session
        # R3.2
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
        """R3.3"""
        # Open the logout page to invalidate any logged-in session
        # R3.3
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
        """R3.4"""
        # Open the logout page to invalidate any logged-in session
        # R3.4
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
    def test_form_sell(self, *_):
        """Validate sell form and fields name, quantity, price, exp date exist"""
        """R3.6"""
        # Open the logout page to invalidate any logged-in session
        # R3.6
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
        """Validate buy form and fields name, quantity exist"""
        """R3.7"""
        # Open the logout page to invalidate any logged-in session
        # R3.7
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

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_form_update(self, *_):  # R3.8 [GET]
        """Validate update form and fields name, quantity, price, exp date exist"""
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
        self.assert_element("#name_update")
        self.assert_element("#quantity_update")
        self.assert_element("#price_update")
        self.assert_element("#exp_date_update")

    # Validate that the ticket-update form can be posted to /update
    # test case R3.11
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
        #Open back up proflile page
        self.open(base_url)
        self.click('input[type="submit"]')
        self.open(base_url + '/update')

    # Validate that the ticket-selling form can be posted to /sell
    # test case for R3.9
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
        # fills out sell form
        self.type('#name_sell', 'new_sell_ticket')
        self.type('#quantity_sell', '10')
        self.type('#price_sell', '10')
        self.type('#exp_date_sell', '20201031')

        # submits sell form
        self.click('input[id="submit-sell"]')

        self.open(base_url)
        # verifies form_sell was POSTed to /
        self.assert_element("#form_sell")

    # Validate that the ticket-buying form can be posted to /buy
    # test case R3.10
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
        # fills out buy form
        self.type('#name_buy', 'new_ticket')
        self.type('#quantity_buy', '10')
        self.click('input[id="submit-buy"]')
        self.open(base_url)
        # returns true if form_buy was POSTed
        self.assert_element('#form_buy')


    @patch('qa327.backend.get_user', return_value=test_user)
    def test_not_loggedin(self, *_):
        """If the user hasnt logged in, show the login page"""
        """R1.1"""
        #Open the logout page to invalidate any logged-in session 
        self.open(base_url + '/logout')
        #open the login page
        self.open(base_url + '/login')
        # make sure it shows the proper page and message
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

        
    @patch('qa327.backend.get_user', return_value=test_user)
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
        self.open(base_url + '/login')
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Hi test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

    @patch('qa327.backend.get_user', return_value=test_user)
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
        self.assert_text("Hi test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

    @patch('qa327.backend.get_user', return_value=test_user)
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
        # fill email and password, email is valid and follows guidelines,
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Hi test_frontend", "#welcome-header")

    @patch('qa327.backend.get_user', return_value=test_user)
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
        self.assert_text("Password format is incorrect", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
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
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
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
        self.assert_text("Hi test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4") 
        

    @patch('qa327.backend.get_user', return_value=test_user)
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
        self.assert_element("#message")
        self.assert_text("Email/Password format is incorrect", "#message")

    # Ensure that the login page is showing after the user submits logout. Ensure that none of
    # the pages can be accessed if user tries to type in their address.
    # test case R7.1
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_logout(self, *_):
        self.open(base_url + '/logout')
        self.open(base_url + '/')
        # returns true if correct message is displayed
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
