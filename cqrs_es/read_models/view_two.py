from cqrs_es.es import overloading
from cqrs_es.events import *


class ViewTwo:
    @overloading
    def apply(self, event: Event):
        print('ViewTwo:: Generic handler for event {0}'.format(event))

    @apply.register(AccountCreated)
    def apply_account_created(self, event: AccountCreated):
        print('ViewTwo -> Read Model : Account Created')

    @apply.register(MoneyDesposited)
    def apply_money_deposited(self, event: MoneyDesposited):
        print('ViewTwo -> Read Model : Money Deposited')

    @apply.register(MoneyWithdrawn)
    def apply_money_withdrawn(self, event: MoneyWithdrawn):
        print('ViewTwo -> Read Model : Money Withdrawn')

    @apply.register(SharesBought)
    def apply_shares_bought(self, event: SharesBought):
        print('ViewTwo -> Read Model : Shares Bought')

    @apply.register(SharesSold)
    def apply_shares_sold(self, event: SharesSold):
        print('ViewTwo -> Read Model : Shares Sold')

    @apply.register(AccountClosed)
    def apply_account_close(self, event: AccountClosed):
        print('ViewTwo -> Read Model : Account Closed')

