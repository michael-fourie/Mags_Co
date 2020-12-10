from flask import render_template, request, session, redirect, url_for
from qa327 import app
import qa327.backend as bn
import re



"""
This file defines the front-end part of the service.
It elaborates how the services should handle different
http requests from the client (browser) through templating.
The html templates are stored in the 'templates' folder. 
"""


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='Register')


''' This function is used to check if the password formatting is correct.
Password needs to have at least: 1 uppercase char, 1 lowercase char,
and special char (special chars defined below)
Input: string variable password
Output: string error message'''
def check_special_pass(password):

    specialChar = "!@#$%^&*()_-+=/"

    special = False
    upper = False
    lower = False
    for i in range(len(password)):
        if password[i].isupper():
            upper = True
        if password[i].islower():
            lower = True
        if any(password[i] in word for word in specialChar):
            special = True
    if not upper or not lower or not special or (len(password) < 6):
        return False
    else:
        return True


''' This function is used to check that the email formatting is correct.
We use a regular expression to make sure that all the conditions of 
a regular email address is met. Length of email is also checked.
Input: string variable email
Output: string error message'''
def check_email_format(email):

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if not re.search(regex, email) or len(email) < 3:  # email must be in RFC5322 format
        return False
    else:
        return True


''' This function is used to check if there are spaces in the first or 
last index of the word. 
Input: string word 
Output: boolean '''
def check_spaces(word):

    if word[0] == " " or word[-1] == " ":
        return False
    else:
        return True


''' This function is used to check if the word passed is is only 
alphanumeric (it can only contain letters, numbers or spaces).
Input: string word
Output: Boolean'''
def check_alnum(word):
    for char in range(len(word)):
        if not (word[char].isalnum() or word[char].isspace()):
            return False
    return True


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = ""

    # The passwords do not match
    if password != password2:
        return render_template('register.html', message="The passwords do not match")

    # The email format and email length is wrong
    if not check_email_format(email):
        return render_template('register.html', message="Email format is incorrect")

    # The password format is wrong
    if not check_special_pass(password):
        return render_template('register.html', message="Password format is incorrect")

    # Name is less than 2 characters or longer than 20 character
    if len(name) <= 2 or len(name) >= 20:
        return render_template('register.html', message="Name length formatting error")

    # Name has special char
    if not check_alnum(name):
        return render_template('register.html', message="Name contains special characters")

    # Space error
    if not check_spaces(name):
        return render_template('register.html', message="Invalid spaces found in word")

    # No errors, so no returns on function has been called, so no issue with validity of credentials
    user = bn.get_user(email)
    if user:
        error_message = "This email has already been used"  # changed error message to satisfy requirement
    elif not bn.register_user(email, name, password, password2):  # new instance of user created
        error_message = "Failed to store user info."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.

    if error_message != "":
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = bn.login_user(email, password)
    """
    Validation for email/password. We must check for blank email or password, 
    invalid password, and invalid email
    """
    if email == "" or password == "":
        return render_template('login.html', message="Email/password cant be blank")

    # "Email format is incorrect" should be error message
    if not check_email_format(email):
        return render_template('login.html', message="Email format is incorrect")

    # Password format is wrong
    if not check_special_pass(password):
        return render_template('login.html', message="Password format is incorrect")

    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between browser and the end server. Typically it is encrypted 
        and stored in the browser cookies. They will be past 
        along between every request the browser made to this services.

        Here we store the user object into the session, so we can tell
        if the client has already login in the following sessions.

        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
        
    return redirect('/')


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object

    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.

    To wrap a function, we can put a decoration on that function.
    Example:

    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            user = bn.get_user(email)
            if user:
                # if the user exists, call the inner_function
                # with user as parameter
                return inner_function(user)
        else:
            # else, redirect to the login page
            return redirect('/login')

    wrapped_inner.__name__ = inner_function.__name__        # Added to make authenticate work
    # Above: this allows other functions to use the authenticate function
    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/')
@authenticate
def profile(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals
    tickets = bn.get_all_tickets()
    return render_template('index.html', user=user, tickets=tickets)


@app.route('/*')
def error():
    return redirect('/', code=404)


''' This function checks the quantity/price of a ticket and makes sure 
it is in the valid length range.
Input: valid range and int ticket quantity/price
Output: boolean'''
def check_quantity(low,high,item):

    if item <= low or item >= high:
        return False
    else:
        return True


@app.route('/sell', methods=["POST"])
@authenticate  # Needed to access instance of user
def sell_ticket(user):
    ticket_name = request.form.get('name')
    ticket_quantity = request.form.get('quantity')
    error_message = ""

    # There must not be a space at beginning or end, and the name mus tbe alphanumeric
    if not check_spaces(ticket_name):
        return render_template('index.html', user=user, message="Invalid spaces found in word")

    # Ticket name must be shorter than 60 characters
    if len(ticket_name) > 60:
        return render_template('index.html', user=user, message="Ticket name is too long")

    # Ticket quantity must be greater than 0 and less than or equal to 100
    if not check_quantity(1, 101, ticket_quantity):
        return render_template('index.html', user=user, message="Invalid quantity of tickets")

    if error_message != "":
        return render_template('index.html', user=user, message=error_message)

    ticket = bn.get_tickets(ticket_name)

    if not check_quantity(9, 101, ticket.price):
        return render_template('index.html', user=user, message="Invalid quantity of tickets")

    # Ticket date must be in valid format - YYYYMMDD
    # Assumption: ticket dates will start from today (2020-11-26) and go onwards
    if (int(ticket.date[:4]) < 2020 or int(ticket.date[4:6]) < 0 or int(ticket.date[4:6]) > 12 or
    int(ticket.date[6:]) < 0 or int(ticket.date[4:6]) > 31):
        return render_template('index.html', user=user, message="Invalid ticket date")

    if error_message != "":
        return redirect('/', message=error_message)
    else:
        # Add the ticket to the user's list of tickets.
        bn.register_ticket(ticket.date, ticket.name, ticket.quantity, ticket.price, ticket.date)
        return render_template('buy.html', user=user, ticket=ticket)


@app.route('/buy', methods=['POST'])
@authenticate  # Needed to access instance of user
def buy_ticket(user):
    ticket_name = request.form.get('name')
    ticket_quantity = request.form.get('quantity')
    error_message = ""

    # ticket contains invalid spaces
    if not check_spaces(ticket_name):
        return render_template('index.html', user=user, message="Invalid spaces found in word")

    # Check if ticket name is only alphanumeric
    if not check_alnum(ticket_name):
        return render_template('index.html', user=user, message="Name contains invalid characters")

    # ticket name is longer than 60 chars
    if len(ticket_name) > 60:
        return render_template('index.html', user=user, message="Ticket name is too long")

    # Ticket quantity must be greater than 0 and less than or equal to 100
    if not check_quantity(1, 101, int(ticket_quantity)):
        return render_template('index.html', user=user, message="Invalid quantity of tickets")

    ticket = bn.get_ticket(ticket_name)   # have a try catch error here?

    # ticket quantity has to be more than quantity requested to buy
    if int(ticket_quantity) > ticket.quantity:
        return render_template('index.html', user=user, message="Requested quantity larger than available tickets")

    # user has to have more balance than ticket price + xtra fees
    if user.balance < (ticket.price * int(ticket_quantity) * 1.35 * 1.05):
        return render_template('index.html', user=user, message="User balance not enough for purchase")

    # redirect and display error message if possible
    if error_message != "":
        return redirect('/', message=error_message)
    else:  # add ticket to user's profile
        bn.register_ticket(ticket.date, ticket.name, ticket.quantity, ticket.price, ticket.date)
        # Check if this works
        ticket_list = bn.get_all_tickets()  # get all tickets and display sell.html (?)
        # Now shows updated tickets for user and redirects to sell page
        return render_template('index.html', user=user, message="Ticket bought successfully")


@app.route('/update')
@authenticate  # Needed to access instance of user
def update_ticket(user):
    # This function will display the update ticket page to the user
    # We need the user information and the ticket information
    # This will then display the update.html page

    ticket_name = request.form.get('name')  # using name but should id be used instead?
    ticket_quantity = request.form.get('quantity')

    error_message = ""

    # There must not be a space at beginning or end
    if not check_spaces(ticket_name):
        return render_template('index.html', user=user, message="Invalid spaces found in ticket name")

    # The name must be alphanumeric
    if not check_alnum(ticket_name):
        return render_template('index.html', user=user, message="Name contains special characters")

    # The name of the ticket is no longer than 60 characters
    if len(ticket_name) > 60:
        return render_template('index.html', user=user, message="Ticket name too long")

    # The quantity of the tickets has to be more than 0, and less than or equal to 100
    if not check_quantity(1, 101, ticket_quantity):
        return render_template('index.html', user=user, message="Invalid quantity of tickets")  # CHANGE REROUTE TO /UPDATE????

    ticket = bn.get_ticket(ticket_name)

    # The ticket of the given name must exist
    if ticket is None:
        return render_template('index.html', user=user, message="Ticket does not exist")

    # Price has to be of range [10, 100]
    if not check_quantity(9, 101, ticket_quantity):
        return render_template('index.html', user=user, message="Invalid ticket price")

    # Date must be given in format YYYYMMDD
    if (int(ticket.date[:4]) < 2020 or int(ticket.date[4:6]) < 0 or int(ticket.date[4:6]) > 12 or
            int(ticket.date[6:]) < 0 or int(ticket.date[4:6]) > 31):
        return render_template('index.html', user=user, message="Invalid ticket date")

    # For any errors, redirect back to / and show an error message
    if error_message != "":
        return redirect('index.html', user=user, message=error_message)
    # If there are no errors?
