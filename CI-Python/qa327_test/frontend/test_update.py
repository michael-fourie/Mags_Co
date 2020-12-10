import pytest
from seleniumbase import BaseCase
from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User, Form, Ticket
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
test_ticket = Ticket(
    name='t1',
    price=100,
    quantity=2,
    email='test123@email.com',
    date='20200223'
)

test_tickets = [
    Ticket(name='t1', price=100, quantity=2, email='test1@email.com', date='20200223'),
    Ticket(name='t2', price=110, quantity=10, email='test2@gmail.com', date='20200314')
 ]

class FrontEndBuyTest(BaseCase):
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_update_invalid_name_alnum(self, *_):
        """ R5.1A The name of the ticket has to be alphanumeric-only, and space
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
        self.type("#name_update", "I_valid")
        # Type in ticket quantity
        self.type("#quantity_update", "5")
        # Type in ticket price
        self.type("#price_update", "15")
        # Type in ticket expiration date
        self.type("#exp_date_update", "20200223")
        # click submit button for update
        self.click("#submit-update")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Name contains special characters", "#message")
        """
        README:
        Have been using this test case above to try to figure ou tbutton issue. 
        I just have all the test cases written below and will then complete 
        them when the button issue has been figured out, so disregard all the 
        test cases below.
        """
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_update_invalid_name_spaces(self, *_):
        """ R5.1B The name of the ticket can have spaces allowed only
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
        self.type("#name_update", "Invalid ")
        # Type in ticket quantity
        self.type("#quantity_update", "5")
        # Type in ticket price
        self.type("#price_update", "15")
        # Type in ticket expiration date
        self.type("#exp_date_update", "20200223")
        # click submit button for update
        self.click("#submit-update")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Invalid spaces found in ticket name", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_update_invalid_name_long(self, *_):
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
        self.type("#name_update",
                  "InvalidInvalidInvalidInvalidInvalidInvalidInvalidInvalidInvalidInvalidInvalidInvalid")
        # Type in ticket quantity
        self.type("#quantity_update", "5")
        # Type in ticket price
        self.type("#price_update", "15")
        # Type in ticket expiration date
        self.type("#exp_date_update", "20200223")
        # click submit button for update
        self.click("#submit-update")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Ticket name is too long", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_update_invalid_quantity_neg(self, *_):
        """ R5.3A The quantity of the tickets has to be more than 0."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type valid ticket name
        self.type("#name_update", "Test name")
        # Type invalid ticket quantity
        self.type("#quantity_update", "-1")
        # Type in ticket price
        self.type("#price_update", "15")
        # Type in ticket expiration date
        self.type("#exp_date_update", "20200223")
        # click submit button for update
        self.click("#submit-update")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Invalid quantity of tickets", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_update_invalid_quantity_big(self, *_):
        """ R5.3B The quantity of the tickets has to be less than or equal to 100."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type valid ticket name
        self.type("#name_update", "Test name")
        # Type in invalid ticket quantity
        self.type("#quantity_update", "101")
        # Type in ticket price
        self.type("#price_update", "15")
        # Type in ticket expiration date
        self.type("#exp_date_update", "20200223")
        # click submit button for update
        self.click("#submit-update")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Invalid quantity of tickets", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_update_invalid_price_lower(self, *_):
        """ R5.4A The ticket price has to be in more than or equal to 0."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type valid ticket name
        self.type("#name_update", "Test name")
        # Type in invalid ticket quantity
        self.type("#quantity_update", "80")
        # Type in ticket price
        self.type("#price_update", "-1")
        # Type in ticket expiration date
        self.type("#exp_date_update", "20200223")
        # click submit button for update
        self.click("#submit-update")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Invalid ticket price", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_update_invalid_price_upper(self, *_):
        """ R5.4B The ticket price has to be less than or equal to 100."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type valid ticket name
        self.type("#name_update", "Test name")
        # Type in invalid ticket quantity
        self.type("#quantity_update", "80")
        # Type in ticket price
        self.type("#price_update", "101")
        # Type in ticket expiration date
        self.type("#exp_date_update", "20200223")
        # click submit button for update
        self.click("#submit-update")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Invalid ticket price", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_update_invalid_date(self, *_):
        """ R5.5 The date must be in the format YYYYMMDD."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type valid ticket name
        self.type("#name_update", "Test name")
        # Type in invalid ticket quantity
        self.type("#quantity_update", "80")
        # Type in ticket price
        self.type("#price_update", "90")
        # Type in ticket expiration date
        self.type("#exp_date_update", "Feb 22 2020")
        # click submit button for update
        self.click("#submit-update")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Invalid ticket date", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=None)
    def test_update_name_does_not_exist(self, *_):
        """ R5.6 The ticket name must exist."""
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open home page
        self.open(base_url)
        # Type valid ticket name
        self.type("#name_update", "hello123")
        # Type in invalid ticket quantity
        self.type("#quantity_update", "80")
        # Type in ticket price
        self.type("#price_update", "90")
        # Type in ticket expiration date
        self.type("#exp_date_update", "20200223")
        # click submit button for update
        self.click("#submit-update")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Ticket does not exist", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_update_ticket_success(self, *_):
        """The user is successful in buying a ticket"""
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
        self.type("#name_update", "t1")
        # Type in ticket quantity
        self.type("#quantity_update", "2")
        # Type in ticket price
        self.type("#price_update", "90")
        # Type in ticket expiration date
        self.type("#exp_date_update", "20200223")
        # click submit button for udate
        self.click("#submit-update")
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("Successfully updated", "#message")