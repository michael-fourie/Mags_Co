import pytest
import qa327.backend as bn
from qa327.models import Ticket
from qa327.models import db

# Mock a sample ticket
test_ticket = Ticket(
    id=100,
    email="test_user@testing.com",
    date='20201210',
    name="t1",
    price=25,
    quantity=3
)

@pytest.mark.usefixtures('server')
def test_get_ticket_valid():
    # First clear teh database of tickets so that IntegrityError is not encountered
    db.session.query(Ticket).delete()
    db.session.commit()
    # Set up valid ticket
    bn.sell_ticket(test_ticket.id, test_ticket.name, test_ticket.quantity, test_ticket.price, test_ticket.date, test_ticket.email)

    # Test if the ticket posted for sale is in the database
    result = bn.get_ticket(test_ticket.name)
    assert result is not None
    assert result.name == test_ticket.name

@pytest.mark.usefixtures('server')
def test_get_ticket_valid():
    # Create a random test ticket id that is not valid or present in the database
    invalid_ticket_id = -1000
    result = bn.get_ticket(invalid_ticket_id)
    assert result == None