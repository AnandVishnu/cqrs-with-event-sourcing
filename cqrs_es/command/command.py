from abc import ABC, abstractmethod
import attr
from cqrs_es.events import *
import uuid



class Command:
    def __init__(self, version):
        self.expected_version = version
        self.name = 'Command'
    def __str__(self):
        return self.name

    def to_event(self):
        raise NotImplementedError()

class CreateAccount(Command):
    def __init__(self, version, name, id, initial_amount=0):
        super().__init__(version)
        self.account_name = name
        self.id = id
        self.amount = initial_amount
        self.name = 'CREATE_NEW_ACCOUNT'

    def to_event(self):
        return [AccountCreated(self.account_name, self.id, self.amount)]

class DepositMoney(Command):
    def __init__(self, version, id, amount):
        super().__init__(version)
        self.id = id
        self.amount = amount
        self.name = 'DEPOSIT_MONEY_INTO_ACCOUNT'

    def to_event(self):
        return [MoneyDesposited(self.id, self.amount)]

class WithdrawMoney(Command):
    def __init__(self, version, id, amount):
        super().__init__(version)
        self.id = id
        self.amount = amount
        self.name = 'WITHDRAW_MONEY_FROM_ACCOUNT'

    def to_event(self):
        return [MoneyWithdrawn(self.id, self.amount)]

class CloseAccount(Command):
    def __init__(self, version, account_id, shares):
        super().__init__(version)
        self.id = account_id
        self.name = 'CLOSE_ACCOUNT'
        self.shares = shares

    def to_event(self):
        return [
            SharesSold(self.id, self.shares),
            MoneyWithdrawn(self.id),
            AccountClosed(self.id)
        ]

class BuyShares(Command):
    def __init__(self, version, id, shares):
        super().__init__(version)
        self.id = id
        self.shares = shares
        self.name = 'BUY_SHARES'

    def to_event(self):
        return [SharesBought(self.id, self.shares)]

class SellShares(Command):
    def __init__(self, version, id, shares):
        super().__init__(version)
        self.id = id
        self.shares = shares
        self.name = 'SELL_SHARES'

    def to_event(self):
        return [SharesSold(self.id, self.shares)]







