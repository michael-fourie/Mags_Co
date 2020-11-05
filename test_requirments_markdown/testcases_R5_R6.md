Test Data:

test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='test_ticket_yo',
    quantity=10,
    price=10,
    date='20200901'
)

test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)

# Test case R5.1: 
### The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
Mocking:
* mock backend.get_ticket to return a test_ticket instance
Actions:
* open /update
* validate test_ticket.name doesn't start or end with space
* if true, also validate test_ticket.name only contains alphanumeric characters

# Test case R5.2:
### The name of the ticket is no longer than 60 characters
mocking:
* mock backend.get_ticket to return a test_ticket instance
Actions: 
* open /update
* validate test_ticket name.length is less than 60 characters.

# Test case R5.3:
### The quantity of the tickets has to be more than 0, and less than or equal to 100.
Mocking:
* mock backend.get_ticket to return test_ticket instance
Actions:
* open /update
* validate test_ticket.quantity is greater than 0 and test_ticket.quantity is less than or equal to 100


# Test case R5.4:
### Price has to be of range [10, 100]
Mocking:
* mock backend.get_ticket to return test_ticket instance
Actions:
* open /update
* validate test_ticket.price is at least 10 and test_ticket.price is at most 100

# test case R5.5:
### Date must be given in the format YYYYMMDD (e.g. 20200901)
Mocking:
* mock backend.get_ticket to return test_ticket instance
Actions:
* open /update
* validate ticket's #date element is in year-month-date format

# test case R5.6:
### The ticket of the given name must exist
Mocking:
* mock backend.get_all_tickets to return all_tickets
* mock backend.get_ticket to return test_ticket instance 
Actions:
* open /update
* validate ticket's #name element exists in database

# test case R5.7
### For any errors, redirect back to / and show an error message
mocking:
* mock backend.get_user to return test_user instance

Actions:
- open /update
- if unhandled error, validate that "not working" is displayed
- validate user is redirected to /

# Test case R6
Constraint: verification does not always pass

# Test case R6.1:
### The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
Mocking:
* mock backend.get_ticket to return test_ticket instance
* mock backend.get_user to return test_user instance
Actions:
* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* open /buy
* validate spaces do not occur at beginning or end of test_ticket's name
* validate rest of test_ticket's name contain only alphanumeric characters or spaces
* open /logout (clean up)

# Test case R6.2:
### The name of the ticket is no longer than 60 characters
Mocking:
* mock backend.get_ticket to return test_ticket
* mock backend.get_user to return test_user instance
Actions:
* open /logout
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* open /buy
* validate that name of ticket is less than 60 characters
* 

# Test case R6.3:
### The quantity of the tickets has to be more than 0, and less than or equal to 100.
Marking:
* mock backend.get_ticket to return test_ticket
Actions:
* open /logout
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* open /buy 
* validate that ticket's #quantity element is at least one but no more than 100.
* open /logout

# Test Case R6.4:
### The ticket name exists in the database and the quantity is more than the quantity requested to buy - positive case
Mocking:

* Mock backend.get_user to return a test_user instance
* Mock backend.get_ticket to return a test_ticket instance
Actions:

* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* enter test_ticket's name into element #buy_name
* enter test_ticket's quantity into element #buy_quantity
* click element #buy_submit
* validate that the #buy_message element shows successful
* open /logout (clean up)

# Test case R6.4
### The ticket name exists in the database and the quantity is more than the quantity requested to buy - negative case
Mocking:
* Mock backend.get_user to return a test_user instance
* Mock backend.get_ticket to return a test_ticket instance
Actions:
* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* enter test_ticket's name into element #buy_name
* enter test_ticket's quantity into element #buy_quantity
* click element #buy_submit
* validate that the #buy_message element shows unsuccesfull
* open /

# Test Case R6.5
### The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%)
Mocking:
* mock backend.get_ticket to return test_ticket
Actions:
* open /logout
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* open /account balance
* store account balance as new variable balance
* open /buy
* store test_ticket.price * quantity + 35% + 5% as new variable total
* validate that balance is greater or equal to total

# Test case R6.7
### For any errors, redirect back to / and show an error message

Mocking:
* mock backend.get_ticket to return test_ticket
* mock backend.get_user to return test_user instance
Actions:
* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* open /buy
* if unhandled error, validate that error message is displayed
* open /
 
