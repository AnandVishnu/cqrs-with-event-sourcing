from cqrs_es.bus import Bus
from cqrs_es.command import *
from cqrs_es.es import Repository, EventStore
from cqrs_es.domain.trading_account import TradingAccount
from cqrs_es.domain.trading_account_handler import TradingAccountHandler
from cqrs_es.domain.order import Order
from cqrs_es.market import Market
from cqrs_es.read_models.view_one import ViewOne
from cqrs_es.read_models.view_two import ViewTwo
import uuid
import time


if __name__ == '__main__':
    # bootstrap bus
    market = Market()
    bus = Bus(market)
    storage = EventStore(bus)
    rep = Repository(storage, bus, TradingAccount)


    handler = TradingAccountHandler(rep)

    # there are 2 views.  All views are just projections of the events
    # each view will have its own table for fast retrival and to avoid any join (denormalised)
    # views are part of read model
    view_one = ViewOne()
    view_two = ViewTwo()

    domain_commands = [
        'CREATE_NEW_ACCOUNT',
        'DEPOSIT_MONEY_INTO_ACCOUNT',
        'WITHDRAW_MONEY_FROM_ACCOUNT',
        'CLOSE_ACCOUNT',
        'BUY_SHARES',
        'SELL_SHARES'
    ]

    domain_events = [
       'ACCCOUNT_CREATED',
        'MONEY_DEPOSITED',
        'MONEY_WITHDRAWN',
        'ACCOUNT_CLOSED',
        'SHARES_BOUGHT',
        'SHARES_SOLD'
    ]
    # commands
    bus.register_commands(domain_commands, handler.handle)
    bus.register_events(domain_events, view_one.apply)
    bus.register_events(domain_events, view_two.apply)


    # start playing command
    account_id = str(uuid.uuid1())
    account_name = 'Tower_Research'

    account = bus.send_command(CreateAccount(-1, account_name, account_id))
    print("------------ Status of the cart after Step 1 -------------")
    print(account)
    market.tick()
    account = bus.send_command(DepositMoney(0, account_id, 1000000))
    print("------------ Status of the cart after Step 2-------------")
    print(account)
    market.tick()
    account = bus.send_command(WithdrawMoney(1, account_id, 1000000))
    print("------------ Status of the cart after Step 3 -------------")
    print(account)
    market.tick()
    account = bus.send_command(DepositMoney(2, account_id, 5000000))
    print("------------ Status of the cart after Step 4 -------------")
    print(account)
    market.tick()

    shares_transaction = [
        Order(symbol='APPL', quantity=1000, market_price=market.get_price('APPL')),
        Order(symbol='GOOG', quantity=1000 , market_price=market.get_price('GOOG'))
    ]
    account = bus.send_command(BuyShares(3, account_id, shares_transaction))
    print("------------ Status of the cart after Step 5 -------------")
    print(account)

    account_id_two = str(uuid.uuid1())
    account_name_two = 'Sunrise Capitals'
    account_two = bus.send_command(CreateAccount(-1, account_name_two, account_id_two ))
    account_two = bus.send_command(DepositMoney(0, account_id_two, 5000000))
    account_two = bus.send_command(BuyShares(1, account_id_two, shares_transaction))
    market.tick()
    market.tick()
    market.tick()
    market.tick()
    market.tick()
    time.sleep(2)


    shares_transaction = [
        Order(symbol='APPL', quantity=1000, market_price=market.get_price('APPL')),
        Order(symbol='GOOG', quantity=1000, market_price=market.get_price('GOOG'))
    ]
    account = bus.send_command(SellShares(4, account_id, shares_transaction))

    print("------------ Status of the cart after Step 6 -------------")
    print(account)
    market.tick()

    shares_transaction = [
        Order(symbol='APPL', quantity=2000, market_price=market.get_price('APPL')),
        Order(symbol='GOOG', quantity=1000, market_price=market.get_price('GOOG'))
    ]
    account = bus.send_command(BuyShares(5, account_id, shares_transaction))
    print("------------ Status of the cart after Step 7 -------------")
    print(account)

    shares_transaction = [
        Order(symbol='APPL', market_price=market.get_price('APPL')),
        Order(symbol='GOOG', market_price=market.get_price('GOOG'))
    ]
    account = bus.send_command(CloseAccount(6, account_id, shares_transaction))
    print("------------ Status of the cart after Step 8 -------------")
    print(account)

    # we can replay entire events and get current state of the object
    replayed = rep.replay_history(account_id)
    print(replayed)

    # print the events that lead to the current state of the entity
    # in debug mode have a look in to storage object and you will see it stores all the events that lead
    # to current state
    all_events = ' -> '.join([e.event_data.name for e in storage.event_db[account_id]])
    print('Events on object id {0}'.format(account_id))
    print(all_events)

    print('------------------Read Model Status------------------------')
    view = view_one.get_details_by_id(account_id)
    print(view)





