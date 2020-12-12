White-box testing for the get_ticket method in the backend.

We will be doing the statement coverage method, making sure that every statement is capable of executing correctly. In the get_ticket(name) function, there are two statements. They are as follows.

<code>ticket = Ticket.query.filter_by(name=name).first()  
return ticket</code>

We will be writing two test cases that assure every statement is executed, one where a valid ticket should be returned and one where an invalid ticket (None) should be returned.

# The first function: Valid Ticket
The input needed for this is a validticket instance, thus returning the ticket when the function is called. We get this valid ticket by using the sell_ticket backend method, to list the ticket for sale.
We then verify that the result is not None, and that it is the ticket we listed for sale.

# The second function: Invalid Ticket
The input needed for this is an invalid ticket instance, thus returningNone function is called. We get this invalid ticket by setting a random ticket id that does not exist, and calling the function with this invalid ticket id.
We then verify that the result is  None.


