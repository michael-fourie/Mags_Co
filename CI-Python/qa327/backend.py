from qa327.models import db, User, Ticket
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, redirect

"""
This file defines all backend logic that interacts with database and other services
"""


def get_user(email):
    """
    Get a user by a given email
    :param email: the email of the user
    :return: a user that has the matched email address
    """
    user = User.query.filter_by(email=email).first()
    return user


def login_user(email, password):
    """
    Check user authentication by comparing the password
    :param email: the email of the user
    :param password: the password input
    :return: the user if login succeeds
    """
    # if this returns a user, then the name already exists in database
    user = get_user(email)

    if not user or not check_password_hash(user.password, password):
        return None
    return user




def register_user(email, name, password, password2):
    """
    Register the user to the database
    :param email: the email of the user
    :param name: the name of the user
    :param password: the password of user
    :param password2: another password input to make sure the input is correct
    :return: an error message if there is any, or None if register succeeds
    """

    hashed_pw = generate_password_hash(password, method='sha256')
    # store the encrypted password rather than the plain password
    new_user = User(email=email, name=name, password=hashed_pw, balance=5000)

    db.session.add(new_user)
    db.session.commit()
    return None

def get_ticket(name):
    """Get a ticket by a given ticket name
    :param name: name of the ticket desired
    :return: ticket object with name: name """

    ticket = Ticket.query.filter_by(name=name).first()
    return ticket

def get_all_tickets():
    """Get all instances of tickets available
    :param: none
    :return: list of all ticket instances
    """

    tickets = Ticket.query.all()
    return tickets

def register_ticket(owner, name, quantity, price, date):
    """Register the ticket in the database
    :param owner: The user selling the ticket
    :param name: the name of the ticket
    :param quantity: quantity available of the ticket
    :param price: the price of each ticket
    :param date: the date for ticket use
    :return: an error message if there is any, or None if action succeeds."""

    new_ticket = Ticket(owner=owner, name=name, quantity=quantity, price=price, date=date)

    db.session.add(new_ticket)
    db.session.commit()

    return new_ticket
"""
def get_buy_form(name,quantity):
    buy_form = Form(name=name,quantity=quantity)

    return buy_form
"""

def get_update():
    name = request.form['name_update_changes']
    quantity = request.form['quantity_update_changes']
    price = ['price_update_changes']
    exp_date = ['exp_date_update_changes']
    updated_ticket = Ticket(name,quantity,price,exp_date)
    return updated_ticket

def sell_ticket(name, quantity, price, date, email):
    """
    Create new ticket in the database
    :param ticket_id: the id of the ticket to be updated
    :param name: the name of the ticket
    :param quantity: the amount of tickets for sale
    :param price: the price of the ticket
    :param date: the expiry date of the ticket
    :param user: seller of the ticket
    :return: an error message if there is any, or None if creation succeeds
    """
    ticket = Ticket()
    ticket.name = name
    ticket.quantity = quantity
    ticket.price = price
    ticket.date = date
    ticket.email = email
    db.session.add(ticket)
    db.session.commit()
    return None