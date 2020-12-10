import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User, Form, Ticket

from werkzeug.security import generate_password_hash, check_password_hash
import requests


"""
This file defines all unit tests for the frontend selling functionality.
"""

# Mock a sample user
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('Test_frontend@'),
    balance=500

)

# Mock some sample tickets
test_ticket = Ticket(
    name='t1',
    price=100,
    quantity=2,
    email='test123@email.com',
    date='02/23/2020'
)

test_tickets = [
    Ticket(name='t1', price=100, quantity=2, email='test1@email.com', date='20200223'),
    Ticket(name='t2', price=110, quantity=10, email='test2@gmail.com', date='20200314')
 ]

class FrontEndSellTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_sell_ticket_name_alnum(self, *_):
        """The name of the ticket has to be alphanumeric-only, and space allowed only if its nit
        the first or last character
        R4.1
        """
        #logout to invalidate any logged in session
        self.open(base_url + '/logout')
        #login a user
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        #open the base url
        self.open(base_url)
        #Enter an invalid ticket name
        self.type('#name_sell', " invalid ")
        self.type("#price_sell", 100)
        self.type("#quantity_sell", "2")
        self.type("#exp_date_sell", "20200921")
        self.click('#submit-sell')
        #Assert that the valid error message is shown.
        self.assert_text("Invalid spaces found in word", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_sell_ticket_name_length(self, *_):
        """The name if the ticket is no longer than 60 characters
        R4.2
        """
        # logout to invalidate any logged in session
        self.open(base_url + '/logout')
        # login a user
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open the /sell route
        self.open(base_url)
        # Enter an invalid ticket name
        self.type('#name_sell', "thisnamewillbewaytoolongforitevertobevalidihopeimeanwhatticketwilleverneedanamethatsthislongisthisoversixtycharactersyetidontknowbutletshopeso")
        self.type("#price_sell", 100)
        self.type("#quantity_sell", "2")
        self.type("#exp_date_sell", "20200921")
        self.click('#submit-sell')
        # Assert that the valid error message is shown.
        self.assert_text("Ticket name is too long", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_sell_ticket_valid_quantity(self, *_):
        """The quantity of the tickets has to be more than 0, and less than or equal to 100.
        R4.3
        """
        # logout to invalidate any logged in session
        self.open(base_url + '/logout')
        # login a user
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open the /sell route
        self.open(base_url)
        # Enter an invalid ticket name
        self.type('#name_sell', "ticketname")
        self.type('#quantity_sell', "-1")
        self.type("#price_sell", "15")
        self.type("#exp_date_sell", "20200921")
        self.click('#submit-sell')
        # Assert that the valid error message is shown
        self.assert_text("Invalid quantity of tickets", "#message")

        # logout to invalidate any logged in session
        self.open(base_url + '/logout')
        # login a user
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open the /sell route
        self.open(base_url)
        # Enter an invalid ticket name
        self.type('#name_sell', "ticketname")
        self.type('#quantity_sell', "101")
        self.type("#price_sell", "15")
        self.type("#exp_date_sell", "20200921")
        self.click('#submit-sell')
        # Assert that the valid error message is shown
        self.assert_text("Invalid quantity of tickets", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_sell_ticket_price_range(self, *_):
        """The price has to be of range [10,100]
        R4.4
        """
        # logout to invalidate any logged in session
        self.open(base_url + '/logout')
        # login a user
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open the /sell route
        self.open(base_url)
        # Enter an invalid ticket name
        self.type('#name_sell', "testticket")
        self.type("#quantity_sell", 1)
        self.type("#price_sell", 101)
        self.click('#submit-sell')
        # Assert that the valid error message is shown.
        self.assert_text("Ticket price outside of valid range", "#message")

        # logout to invalidate any logged in session
        self.open(base_url + '/logout')
        # login a user
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open the /sell route
        self.open(base_url)
        # Enter an invalid ticket name
        self.type('#name_sell', "testticket")
        self.type("#quantity_sell", 1)
        self.type("#price_sell", 9)
        self.click('#submit-sell')
        # Assert that the valid error message is shown.
        self.assert_text("Ticket price outside of valid range", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_sell_ticket_valid_date(self, *_):
        """ Date must be given in the format YYYYMMDD (e.g. 20200901)
        R4.5
        """
        # logout to invalidate any logged in session
        self.open(base_url + '/logout')
        # login a user
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open the /sell route
        self.open(base_url)
        # Enter an invalid ticket name
        self.type('#name_sell', "ticketname")
        self.type("#price_sell", 10)
        self.type("#quantity_sell", 1)
        self.type("#exp_date_sell", "09212020")
        self.click('#submit-sell')
        # Assert that the valid error message is shown.
        self.assert_text("Invalid ticket date", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    def test_sell_ticket_redirect_on_error(self, *_):
        """  For any errors, redirect back to / and show an error message
        R4.6
        """
        # logout to invalidate any logged in session
        self.open(base_url + '/logout')
        # login a user
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open the /sell route
        self.open(base_url)
        # Enter an invalid ticket info, should be redirected to / route
        self.type('#name_sell', " invalid ")
        self.type("#price_sell", 1)
        self.type("#quantity_sell", 0)
        self.type("#exp_date_sell", "09212020")
        self.click('#submit-sell')
        self.assert_element("#welcome-header")
        # Assert that the valid error message is shown.
        self.assert_text("Hi test_frontend", "#welcome-header")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_ticket', return_value=test_ticket)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.sell_ticket', return_value=None)
    def test_sell_ticket_posted(self, *_):
        """  The added new ticket information will be posted on the user profile page
        R4.7
        """
        # logout to invalidate any logged in session
        self.open(base_url + '/logout')
        # login a user
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Test_frontend@")
        # click enter button
        self.click('input[type="submit"]')
        # open the /sell route
        self.open(base_url)
        # Enter an invalid ticket info, should be redirected to / route
        self.type('#name_sell', "t1")
        self.type("#price_sell", 100)
        self.type("#quantity_sell", "2")
        self.type("#exp_date_sell", "20200921")
        self.click('#submit-sell')
        self.assert_element("#welcome-header")
        # Assert that the valid error message is shown.
        self.assert_text("Hi test_frontend", "#welcome-header")