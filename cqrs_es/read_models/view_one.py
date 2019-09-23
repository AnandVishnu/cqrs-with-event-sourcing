from cqrs_es.es import overloading
from cqrs_es.events import *
from .account_dto import AccountDTO


class ViewOne:
    def __init__(self):
        self.db = {}

    @overloading
    def apply(self, event: Event):
        print('ViewOne:: Generic handler for event {0}'.format(event))

    @apply.register(AccountCreated)
    def apply_account_created(self, event: AccountCreated):
        print('ViewOne -> Read Model : Account Created')
        acc = AccountDTO(event.id, event.account_name, event.amount)
        self.db[acc.id] = acc

    @apply.register(MoneyDesposited)
    def apply_money_deposited(self, event: MoneyDesposited):
        print('ViewOne -> Read Model : Money Deposited')
        account = self.db[event.id]
        account.deposit(event.amount)

    @apply.register(MoneyWithdrawn)
    def apply_money_withdrawn(self, event: MoneyWithdrawn):
        print('ViewOne -> Read Model : Money Withdrawn')
        account = self.db[event.id]
        account.withdraw(event.amount)

    @apply.register(SharesBought)
    def apply_shares_bought(self, event: SharesBought):
        print('ViewOne -> Read Model : Shares Bought')
        account = self.db[event.id]
        account.add_shares(event.shares)

    @apply.register(SharesSold)
    def apply_shares_sold(self, event: SharesSold):
        print('ViewOne -> Read Model : Shares Sold')
        account = self.db[event.id]
        account.remove_shares(event.shares)

    @apply.register(AccountClosed)
    def apply_account_close(self, event: AccountClosed):
        print('ViewOne -> Read Model : Account Closed')
        account = self.db[event.id]
        account.close_account()

    def get_details_by_id(self, account_id):
        return self.db[account_id]

