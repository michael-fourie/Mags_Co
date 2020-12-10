import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User, Form

from werkzeug.security import generate_password_hash, check_password_hash
import requests

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


class FrontUpdatePageTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets) # do I need?
    def test_alphanum(self, *_):  # R5.1A [POST]
        """ This function checks that the name of the ticket is alpha-numeric only.
        """
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
        # enter name into element
        self.type("#name_update", '$invalid_name$')
        # enter quantity into element
        self.type("#quantity_update", '2')
        # enter price into element
        self.type("#price_update", '100')
        # enter expiration date into elemen
        self.type("#exp_date_update", '02/23/2020')
        # click enter button
        self.click('input[id="submit-update"]')
        # validate error message is shown for special chars
        self.assert_element("#message")
        self.assert_text("Name contains special characters", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_space(self, *_):  # R5.1b [POST]
        """ This function checks that spaces are not in the first or last character.
        """
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
        # enter name into element
        self.type("#name_update", 'a space ')
        # enter quantity into element
        self.type("#quantity_update", '2')
        # enter price into element
        self.type("#price_update", '100')
        # enter expiration date into element
        self.type("#exp_date_update", '02/23/2020')
        # click enter button
        self.click('input[id="submit-update"]')
        # validate error message is shown for special chars
        self.assert_element("#message")
        self.assert_text("Name contains a invalid space", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_name_len(self, *_): # R5.2 [POST]
        """The name of the ticket is no longer than 60 characters.
        """
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
        # enter name into element
        self.type("#name_update", 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')  # 61 a's
        # enter quantity into element
        self.type("#quantity_update", '2')
        # enter price into element
        self.type("#price_update", '100')
        # enter expiration date into element
        self.type("#exp_date_update", '02/23/2020')
        # click enter button
        self.click('input[id="submit-update"]')
        # validate error message is shown for special chars
        self.assert_element("#message")
        self.assert_text("Name is too long", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_quantity(self, *_): # R5.3 [POST]
        """The quantity of the ticket is more than 0 and less than or equal to 100.
        """
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
        # enter name into element
        self.type("#name_update", 'test_name')
        # enter quantity into element
        self.type("#quantity_update", '101')
        # enter price into element
        self.type("#price_update", '100')
        # enter expiration date into element
        self.type("#exp_date_update", '02/23/2020')
        # click enter button
        self.click('input[id="submit-update"]')
        # validate error message is shown for special chars
        self.assert_element("#message")
        self.assert_text("Contains an invalid quantity", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_price(self, *_): # R5.4 [POST]
        """The price of the ticket is in the range [10,100].
        """
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
        # enter name into element
        self.type("#name_update", 'test_name')
        # enter quantity into element
        self.type("#quantity_update", '2')
        # enter price into element
        self.type("#price_update", '101')
        # enter expiration date into element
        self.type("#exp_date_update", '02/23/2020')
        # click enter button
        self.click('input[id="submit-update"]')
        # validate error message is shown for special chars
        self.assert_element("#message")
        self.assert_text("Invalid price", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_date(self, *_): # R5.5 [POST]
        """The date must be given in the format YYYYMMDD.
        """
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
        # enter name into element
        self.type("#name_update", 'test_name')
        # enter quantity into element
        self.type("#quantity_update", '2')
        # enter price into element
        self.type("#price_update", '100')
        # enter expiration date into element
        self.type("#exp_date_update", 'Dec122020')
        # click enter button
        self.click('input[id="submit-update"]')
        # validate error message is shown for special chars
        self.assert_element("#message")
        self.assert_text("Invalid expiration date", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_exist(self, *_):  # R5.6 [POST]
        """The ticket of the given name must exist.
        """


    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_errors(self, *_):  # R5.7 [POST]
        """For any errors, redirect back to / and show error message.
        """
