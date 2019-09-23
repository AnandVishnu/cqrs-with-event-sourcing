from cqrs_es.es import Repository
from cqrs_es.command import *
from .trading_account import TradingAccount
from cqrs_es.es import overloading


class TradingAccountHandler():
    def __init__(self, repo:Repository):
        self.repository = repo

    @overloading
    def handle(self, command:Command):
        print('TradingAccountHandler:: Generic handler for event {0}'.format(command))

    @handle.register(CreateAccount)
    def handle_create_account(self, command: CreateAccount):
        print('Command: {0}'.format(command))
        return self._(command, lambda id : TradingAccount(self.repository.bus.market))


    @handle.register(DepositMoney)
    def handle_deposit_money(self, command: DepositMoney):
        print('Command: {0}'.format(command))
        return self._(command)


    @handle.register(WithdrawMoney)
    def handle_with_money(self, command : WithdrawMoney):
        print('Command: {0}'.format(command))
        return self._(command)


    @handle.register(BuyShares)
    def handle_buy_share(self, command : BuyShares):
        print('Command: {0}'.format(command))
        return self._(command)


    @handle.register(SellShares)
    def handle_sell_share(self, command: SellShares):
        print('Command: {0}'.format(command))
        return self._(command)


    @handle.register(CloseAccount)
    def handle_close_account(self, command: CloseAccount):
        print('Command: {0}'.format(command))
        return self._(command)


    def _(self, command: Command, get_instance=None):
        if get_instance is None:
            get_instance = lambda id: self.repository.get_by_id(id)
        events = command.to_event()
        [print('Event : {0}'.format(e)) for e in events]
        trading_account = get_instance(command.id)
        trading_account.apply_changes(events)
        self.repository.save_event(trading_account, command.expected_version)
        return trading_account






