Test Data:
```sh
test_user = User(
    email='new_test@test.com',
    name='new_test',
    password=generate_password_hash('new_test')
)
```
```sh
test_ticket = Ticket(
    name='new_ticket',
    quantity=10,
    price=10,
    date='20201031'
)
```
```sh
test_sell_form = Form(
    name='new_ticket',
    quantity=10,
    price=10,
    exp_date='20201031'
)
```
```sh
test_buy_form = Form(
    name='new_ticket',
    quantity=10
)
```
=
### Test Case R3.1 - If the user is not logged in, redirect to login page
Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /
- since user is not logged in, authenticate will redirect to /login
- open /login
- validate that current page contains #mesage element

### Test Case R3.2 - This page shows a header 'Hi {}'.format(user.name)
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- validate that current page contains #welcome-header element == 'Hi {}'.format(user.name)

### Test Case R3.3 This page shows user balance.
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- validate that page shows #user_balance element

### Test Case R3.4 - This page shows a logout link, pointing to /logout
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- validate that page contains an href '/logout'

### Test Case R3.5 - This page lists all available tickets. Information including the quantity of each ticket, the owner's email, and the price, for tickets that are not expired.
Mocking:
- mock backend.get_all_ticket to return all_tickets
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- make sure all tickets are displayed
- loop through and check the following from all_tickets:
-- #quantity element is listed and valid
-- #email element of owner is listed
-- #price element is listed and valid
-- #exp_date element is listed valid

### Test Case R3.6 - This page contains a form that a user can submit new tickets for sell. Fields: name, quantity, price, expiration date
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- validate that sell_form contains #name element
- validate that sell_form contains #quantity element
- validate that sell_form contains #price element
- validate that sell_form contains #exp_date element

### Test Case R3.7 - This page contains a form that a user can buy new tickets. Fields: name, quantity
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- validate that buy_form contains #name element
- validate that buy_form contains #quantity element

### Test Case R3.8 - The ticket-selling form can be posted to /sell
Mocking:
- mock backend.get_user to return a test_user instance
- mock backend.test_sell_form to return a sell_form instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- click the input[type="sell"]
- open /sell
- enter sell_form name into element #name
- enter sell_form quantity into element #quantity
- enter sell_form price into element #price
- enter sell_form expiration date into element #exp_date
- submit data with button input[type="submit"]
- validate ticket-selling form is in page


### Test Case R3.9 - The ticket-buying form can be posted to /buy
Mocking:
- mock backend.get_user to return a test_user instance
- mock backend.test_buy_form to return a buy_form instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- click the input[type="buy"]
- open /buy
- enter buy_form name into element #name
- enter buy_form quantity into element #quantity
- submit data with button input[type="submit"]
- validate ticket-buying form is in page

### Test Case R3.10 - The ticket-update form can be posted to /update
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- click the input[type="update"]
- open /update
- validate that ticket-update form is in page

R4	/sell	[POST]
### Test Case R4.1 - The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
Mocking:
- mock backend.get_ticket to return test_ticket instance
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- open /sell
- validate test_ticket #name element of ticket does not start or end with a space
- validate test_ticket #name element only contains alphanumeric characters

### Test Case R4.2 - The name of the ticket is no longer than 60 characters
Mocking:
- mock backend.get_ticket to return test_ticket instance
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- open /sell
- validate test_ticket #name element is 60 characters or less

### Test Case R4.3 - The quantity of the tickets has to be more than 0, and less than or equal to 100.
Mocking:
- mock backend.get_ticket to return test_ticket instance
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- open /sell
- validate test_ticket #quantity element is more than 0 but less than or equal to 100

### Test Case R4.4 - Price has to be of range [10, 100]
Mocking:
- mock backend.get_ticket to return test_ticket instance
- mock backend.get_user to return a test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- open /sell
- validate test_ticket #price element is in range 10-100

### Test Case R4.5 - Date must be given in the format YYYYMMDD (e.g. 20200901)
Mocking:
- mock backend.get_ticket to return test_ticket instance
- mock backend.get_user to return test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- open /sell
- validate test_ticket #date element is in the format YYYMMDD

### Test Case R4.6 - For any errors, redirect back to / and show an error message
Mocking:
- mock backend.get_user to return test_user instance

- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- open /sell
- if unhandled error, validate that "not working" is displayed
- validate user is redirected to /

### Test Case R4.7 - The added new ticket information will be posted on the user profile page
Mocking:
- mock backend.get_ticket to return test_ticket instance
- mock backend.get_user to return test_user instance

Actions:
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- submit data with button input[type="submit"]
- open /
- open /sell
- input information for test_ticket fields
- submit data with button input[type="submit"]
- open /profile
- validate that test_ticket information is posted in profile
