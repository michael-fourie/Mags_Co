import pytest
from seleniumbase import BaseCase
from qa327_test.conftest import base_url


# integration testing: the test case interacts with the
# browser, and test the whole system (frontend+backend).

@pytest.mark.usefixtures('server')
class Posting(BaseCase):

    def register(self):
        """register new user"""
        self.open(base_url + '/register')
        self.type("#email", "testemail@gmail.com")
        self.type("#name", "test0")
        self.type("#password", "Test0@")
        self.type("#password2", "Test0@")
        self.click('input[type="submit"]')

    def login(self):
        """ Login to SeatGeek and verify that login was successful. """
        self.open(base_url + '/login')
        self.type("#email", "testemail@gmail.com")
        self.type("#password", "Test0@")
        self.click('input[type="submit"]')

    def post(self):
        """Create a ticket to sell and list it for sale"""
        self.open(base_url)
        self.type('#name_sell', "t1")
        self.type("#price_sell", "100")
        self.type("#quantity_sell", "2")
        self.type("#exp_date_sell", "20200921")
        self.click('#submit-sell')

    def logout(self):
        """After succesfully creating a posting, log the user out"""
        self.open(base_url + '/logout')

    def test_successful_post(self):
        """Test whether the posting of the ticket is successful"""
        self.register()
        self.login()
        self.post()
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("Hi test0", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100 2 testemail@gmail.com 20200921", "#tickets div h4")
        self.logout()
