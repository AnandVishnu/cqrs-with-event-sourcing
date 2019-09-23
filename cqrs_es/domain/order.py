import attr
import sys

@attr.s
class Order:
    symbol = attr.ib()
    quantity = attr.ib(default=sys.maxsize)
    market_price = attr.ib(default=-1)