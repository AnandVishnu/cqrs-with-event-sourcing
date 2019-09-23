from datetime import datetime
from dateutil.relativedelta import relativedelta

class AccountDTO():
    def __init__(self, id, name, bal):
        self.name = name
        self.id = id
        self.balance = bal
        self.shares = {}
        self.closed = False
        self.account_opening_date = datetime.now()
        self.account_closing_date = datetime.now() + relativedelta(years=100)

    def __str__(self):
        return \
            ' <account name> : {0}, <account balance> :{1}, <shares> : {2} , <active> : {3} \n' \
            '<account opening date> : {4}, <account closing date>: {5}' \
                .format(self.name, self.balance, ','.join(self.shares), not self.closed,
                        self.account_opening_date, self.account_closing_date)

    def deposit(self, balance):
        self.balance = self.balance + balance

    def withdraw(self, balance):
        self.balance = self.balance - balance

    def add_shares(self, share_infos):
        total_cost = 0
        for share in share_infos:
            if share.symbol not in self.shares:
                self.shares[share.symbol] = 0

            total_cost = total_cost + share.market_price * share.quantity
            self.shares[share.symbol] = self.shares[share.symbol] + share.quantity

        self.balance = self.balance - total_cost

    def remove_shares(self, share_infos):
        total_cost = 0
        for share in share_infos:
            self.shares[share.symbol] = self.shares[share.symbol] - share.quantity
            if self.shares[share.symbol] == 0:
                self.shares.pop(share.symbol, None)

            total_cost = total_cost + share.market_price * share.quantity

        self.balance = self.balance + total_cost


    def close_account(self):
        self.closed = True
        self.account_closing_date = datetime.now()


