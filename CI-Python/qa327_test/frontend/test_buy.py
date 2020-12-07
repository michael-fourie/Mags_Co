import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User, Form

from werkzeug.security import generate_password_hash, check_password_hash
import requests


"""
This file defines all buy function unit tests for the frontend homepage.

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

# Mock a user that will not have enough money to buy a ticket
test_poor_user = User(
    email='test_poor@test.ca',
    name='namepoor',
    password=generate_password_hash('Name_register@1'),
    balance=10
    )

# Mock some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100', 'quantity': '2', 'email': 'test123@email.com', 'date': '02/23/2020'}
]

# Mock a sample sell form
test_sell_form = Form(
    name='sell_tix',
    quantity='2',
    price='50',
    date='02/23/2020'
)

# Mock a sample buy form
test_buy_form = Form(
    name='buy_tix',
    quantity='2',
    price='50',
    date='02/23/2020'
)


class FrontEndBuyTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_tickets)
    def test_invalid_name_alnum(self, *_):
        """ R6.1A The name of the ticket has to be alphanumeric-only, and space
        allowed only if it is not the first or the last character."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type invalid ticket name
        self.type("#name_buy", "I_valid")
        # Type in ticket quantity
        self.type("#quantity_buy", "5")
        # click submit button for buy
        self.click("#submit-buy")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Word contains invalid characters", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_tickets)
    def test_invalid_name_spaces(self, *_):
        """ R6.1B The name of the ticket can have spaces allowed only
        if it is not the first or the last character."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type invalid ticket name
        self.type("#name_buy", "Invalid ")
        # Type in ticket quantity
        self.type("#quantity_buy", "5")
        # click submit button for buy
        self.click('input[id="form_buy"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Invalid spaces found in word", "#message")

        @patch('qa327.backend.get_user', return_value=test_user)
        @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
        @patch('qa327.backend.get_ticket', return_value=test_tickets)
        def test_invalid_name_long(self, *_):
            """ R6.2 The name of the ticket is no longer than 60 characters."""
            self.open(base_url + '/logout')
            self.open(base_url + '/login')
            # fill email and password
            self.type("#email", "test_frontend@test.com")
            self.type("#password", "Test_frontend@")
            # click enter button
            self.click('input[type="submit"]')
            # open home page
            self.open(base_url)
            # Type invalid ticket name
            self.type("#name_buy",
                      "InvalidInvalidInvalidInvalidInvalidInvalidInvalidInvalidInvalidInvalidInvalidInvalid")
            # Type in ticket quantity
            self.type("#quantity_buy", "5")
            # click submit button for buy
            self.click('input[id="form_buy"]')
            # make sure it shows proper error message
            self.assert_element("#message")
            self.assert_text("Ticket name is too long", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_tickets)
    def test_invalid_quant_neg(self, *_):
        """ R6.3A The quantity of the tickets has to be more than 0."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type invalid ticket name
        self.type("#name_buy", "Test name")
        # Type in ticket quantity
        self.type("#quantity_buy", "-1")
        # click submit button for buy
        self.click('input[id="form_buy"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Invalid quantity of tickets", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_tickets)
    def test_invalid_quant_big(self, *_):
        """ R6.3B The quantity of the tickets has to be less than or equal to 100."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type invalid ticket name
        self.type("#name_buy", "Test name")
        # Type in ticket quantity
        self.type("#quantity_buy", "101")
        # click submit button for buy
        self.click('input[id="form_buy"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Invalid quantity of tickets", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_tickets)
    def test_invalid_quant_neg(self, *_):
        """ R6.4A The ticket name exists in the database."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type invalid ticket name
        self.type("#name_buy", "No ticket")
        # Type in ticket quantity
        self.type("#quantity_buy", "-1")
        # click submit button for buy
        self.click('input[id="form_buy"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Ticket not found in database.", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_tickets)
    def test_invalid_quant_neg(self, *_):
        """ R6.4B The ticket quantity is more than the quantity requested to buy."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type invalid ticket name
        self.type("#name_buy", "t1")
        # Type in ticket quantity
        self.type("#quantity_buy", "3")
        # click submit button for buy
        self.click('input[id="form_buy"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Requested quantity larger than available tickets", "#message")

    @patch('qa327.backend.get_user', return_value=test_poor_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_tickets)
    def test_invalid_quant_neg(self, *_):
        """ R6.5 The user has more balance than the ticket price * quantity
        + service fee (35%) + tax (5%)"""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_poor@test.ca")
        self.type("#password", "Name_register@1")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type invalid ticket name
        self.type("#name_buy", "t1")
        # Type in ticket quantity
        self.type("#quantity_buy", "10")
        # click submit button for buy
        self.click('input[id="form_buy"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("User balance not enough for purchase", "#message")






