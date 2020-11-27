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


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = ""

    # for validation:
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    specialCharacters = "!@#$%^&*+=~`-_/"

    #The passwords do not match
    if password != password2:
        print("pass no mathc")
        error_message = "The passwords do not match"

    #The email too short
    if len(email) < 1:
        print("short email")
        error_message = "Email format error"

    #The email format is wrong
    if not re.search(regex, email):  # email must be in RFC5322 format
        print("invalid email")
        error_message = "Email not in RFC5322 format"

    #Password to short
    if len(password) < 6:  # changed to < 6 to satisfy length requirement
        print("pass to short")
        error_message = "Password not long enough"

    #Password not valid
    if len(password) > 5:  # check to make password is complex enough
        print("check valid pass")
        upper = False
        lower = False
        special = False
        for char in range(len(password)):
            if password[char].isupper():
                upper = True
            if password[char].islower():
                lower = True
            if any(password[char] in word for word in specialCharacters):
                special = True
        if not upper and not lower and not special:
            error_message = "Password is not strong enough"

    #Name is too short
    if len(name) <= 2:  # name is less than 2 characters or longer than 20 characters
        print("name to short")
        error_message = "Name length formatting error"

    #Name is too long
    if len(name) >= 20:
        print("name to long")
        error_message = "Name length formatting error"

    #Name has special char
    if len(name) > 0:  # name is not alpha-numeric
        print("name spec char")
        for char in range(len(name)):
            if (not name[char].isalnum()) or (name[char].isspace()):
                error_message = "Name contains special characters"


    #Space error
    if name[0] == " " or name[-1] == " ":  # spaces are in the first or last index of string
        print("space err")
        error_message = "Spacing error in name"

    #No error message, so no issue with validity of credentials
    if error_message == "":
        user = bn.get_user(email)
        if user:
            error_message = "This email has already been used"  # changed error message to satisfy requirement
        elif not bn.register_user(email, name, password, password2):  # new instance of user created
            error_message = "Failed to store user info."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.


    if error_message != "":
        print("if error messg")
        return render_template('register.html', message=error_message)
    else:
        print("redirect")
        return redirect('/login')


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = bn.login_user(email, password)
    print(user)
    """
    Validation for email/password. We must check for blank email or password, 
    invalid password, and invalid email
    """
    if email == "" or password == "":
        return render_template('login.html', message="Email/password cant be blank")

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        return render_template('login.html', message="Email/Password format is incorrect")

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
        return render_template('login.html', message="Email/Password format is incorrect")

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

@app.route('/buy')
# @authenticate  # (??) not sure if we need this here to authenticate user
def buy_ticket(user):
    # This function will display the buy ticker page to the user
    # We need the user information and the ticker information
    # This will then display the buy.html page
    ticket = bn.get_all_tickets()
    return render_template('buy.html', user=user, ticket=ticket)


@app.route('/sell') # THIS APP ROUTE MAY NEED TO BE INDEX APP ROUTE
# @authenticate  # (??) not sure if we need this here to authenticate user
def sell_ticket(user):
    '''THIS IS ACTUALLY CODE FOR BUY_TICKET'''
    # This function will display the buy ticker page to the user
    # We need the user information and the ticker information
    # This will then display the sell.html page
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    error_message = ""

    # ticket contains invalid spaces, or ticket is not alphanumeric
    if name[0] == " " or name[-1] == " " or not ticket_name.isalnum():
        error_message = "Invalid ticket name"

    # ticket name is longer than 60 chars
    if len(name) > 60:
        error_message = "Ticket name too long"

    # ticket quantity has to be greater than zero and less than 100
    if ticket_quantity <= 0 or ticket_quantity > 100:
        error_message = "Invalid amount of tickets"

    ticket = bn.get_ticket(name)   # have a try catch error here?

    # ticket quantity has to be more than quantity requested to buy
    if quantity > ticket.quantity:
        error_messsage = "Requested quantity larger than available tickets"

    # user has to have more balance than ticket price + xtra fees
    if user.balance < (ticket.price * quantity * 1.35 * 1.05):
        error_message = "User balance not enough for purchase"

    # redirect and display error message if possible
    if error_message != "":
        return redirect('/', message=error_message)
    else:  # add ticket to user's profile
        error_message = ""     # NEED TO CREATE A TICKET ARRAY IN USER MODEL NOT STRING


    ticket = bn.get_all_tickets()
    return render_template('sell.html', user=user, ticket=ticket)

