import random
class Market:
    def __init__(self):
        self.vol = 0.7

        self.price_dict = {
            'APPL' : 187.61,
            'GOOG' : 1168.9507,
            'FB'   : 202.48
        }

    def tick(self):
        for key in self.price_dict:
            self.price_dict[key] = self.price_dict[key] + self.vol * random.gauss(-1,1)

    def get_price(self, symbol):
        return self.price_dict[symbol]
