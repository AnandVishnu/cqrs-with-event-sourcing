from .aggregate import Aggregate
from cqrs_es.events import *
from cqrs_es.command import *
from typing import List
from cqrs_es.es.utils import overloading
from cqrs_es.market import Market
import sys

class TradingAccount(Aggregate):

    def __init__(self, market=None):
        super().__init__()
        self.market = market
        self.name = None
        self.id = None
        self.balance = None
        self.shares = None
        self.closed = None

    def __str__(self):
        return \
            ' [account name] : {0}, [account balance] :{1}, [shares] : {2} , [active] : {3}'\
                .format(self.name, self.balance, ','.join(self.shares), not self.closed)

    def __repr__(self):
        return self.__str__()

    @overloading
    def apply(self, event: Event):
        print('TradingAccount:: Generic implementation for applying event {0}'.format(event))

    @apply.register(AccountCreated)
    def apply_create_account(self, _event_: AccountCreated):
        self.id = _event_.id
        self.name = _event_.account_name
        self.balance = _event_.amount
        self.closed = False
        self.shares = {}
        self.overdraft = 10000

    @apply.register(MoneyDesposited)
    def apply_money_deposited(self, _event_:MoneyDesposited):
        self.balance = self.balance + _event_.amount

    @apply.register(MoneyWithdrawn)
    def apply_money_withdrawn(self, _event_:MoneyWithdrawn):
        # some kind of checks to see if balance is never -ve
        # when no amount, specified, default to all money
        if _event_.amount is None:
            _event_.amount = self.balance

        self.balance = self.balance - _event_.amount

    @apply.register(SharesBought)
    def apply_buy_shares(self, _event_ : SharesBought):
        orders = _event_.shares
        total_cost = 0
        for order in orders:
            total_cost = total_cost + order.market_price * order.quantity
            if order.symbol not in self.shares:
                self.shares[order.symbol] = 0

            self.shares[order.symbol] = self.shares[order.symbol] + order.quantity

        self.balance = self.balance - total_cost

    @apply.register(SharesSold)
    def apply_sell_shares(self, _event_: SharesSold):
        orders = _event_.shares
        total_cost = 0
        for order in orders:
            # sell everything
            if order.quantity == sys.maxsize:
                order.quantity = self.shares[order.symbol]

            total_cost = total_cost + order.market_price * order.quantity
            if order.symbol not in self.shares:
                self.shares[order.symbol] = 0

            self.shares[order.symbol] = self.shares[order.symbol] - order.quantity
            if self.shares[order.symbol] == 0:
                self.shares.pop(order.symbol, None)

        self.balance = self.balance + total_cost

    @apply.register(AccountClosed)
    def apply_close_account(self, _event_ : AccountClosed):
        self.closed = True


