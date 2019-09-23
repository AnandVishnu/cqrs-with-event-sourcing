from abc import ABC, abstractmethod
import attr
import uuid
from datetime import datetime


class Event:
    def __init__(self):
        self.name = 'Event'
    def __str__(self):
        return self.name


class AccountCreated(Event):
    def __init__(self, name, id, initial_amount=0):
        super().__init__()
        self.id = id
        self.account_name = name
        self.amount = initial_amount
        self.name = 'ACCCOUNT_CREATED'

class MoneyDesposited(Event):
    def __init__(self, id, amount):
        super().__init__()
        self.id = id
        self.amount = amount
        self.name = 'MONEY_DEPOSITED'

class MoneyWithdrawn(Event):
    def __init__(self, id, amount=None):
        super().__init__()
        self.id = id
        self.amount = amount
        self.name = 'MONEY_WITHDRAWN'

class AccountClosed(Event):
    def __init__(self, account_id):
        super().__init__()
        self.id = account_id
        self.name = 'ACCOUNT_CLOSED'

class SharesBought(Event):
    def __init__(self, id, shares):
        super().__init__()
        self.id = id
        self.shares = shares
        self.name = 'SHARES_BOUGHT'

class SharesSold(Event):
    def __init__(self, id, shares):
        super().__init__()
        self.id = id
        self.shares = shares
        self.name = 'SHARES_SOLD'

class EventDescriptor():
    def __init__(self, event_data, version):
        self.event_data = event_data
        self.version = version
        self.id = uuid.uuid4()
        self.timestamp = datetime.now()

# @attr.s
# class EventDescriptor():
#     event_data = attr.ib(type=Event)
#     version = attr.ib(type=int)
#     id = attr.ib(uuid.uuid4())
#     timestamp = attr.ib(default=datetime.now())