import etherscan.stats as stats
import json
import pandas as pd

class Stat:
    def __init__(self, api_key):
        self.api = stats.Stats(api_key = api_key)
        self.price = None

    def get_ether_last_price(self):
        self.price = self.api.get_ether_last_price()
        print(self.price)
        return
    
    def format_price(self):
        if self.price == None:
            print('No price data')
        else:
            price = self.price
            price = pd.DataFrame({'price':[price.get('ethbtc'), price.get('ethusd')], 'time': [price.get('ethbtc_timestamp'), price.get('ethusd_timestamp')]}, index= ['ethbtc','ethusd'], )
            price.time=pd.to_datetime(price.time, unit = 's')
            print(price)
        return

    def get_total_ether_supply(self):
        print(int(self.api.get_total_ether_supply())/10**18)
        return


# with open('section1/task3/key.json', mode='r') as file:
#     key = json.loads(file.read())['key']
# api = Stat(key)
# api.get_ether_last_price()
# api.format_price()
# api.get_total_ether_supply()