import etherscan.accounts as accounts
import etherscan.client as client
import json
import pandas as pd
#  in ertherscan.accounts get_all_transactions() and get_all_blocks_mined() doesn't work
#  get_transcation_page and get_blocks_mined_page will do the same thing

class Account:
    def __init__(self, address, api_key):
        self.address = address
        self.apikey = api_key
        self.api = accounts.Account(address = address, api_key = api_key)
        self.trans, self.mined = None, None

    def add_address(self, add):
        if type(self.address) == str:
            self.address = [self.address]
        if type(add) == str:
            add = [add]
        self.address = list(set(self.address + add))
        self.api = accounts.Account(address=self.address, api_key= self.apikey)

    def get_balance(self):
        # only for single address
        return print(str(int(self.api.get_balance())/10**18) + ' Ether')

    def get_balance_multiple(self):
        result = self.api.get_balance_multiple()
        for i in range(len(result)):
            result[i]['balance'] = str(int(result[i]['balance']) / 10 **18) + ' Ether'

        result = pd.DataFrame(result)
        return print(result)
    
    def get_transaction(self, **kargs):
        # get transcations for a single address
        # params: optional
        # page: 
        # offset: default 10000
        # sort: 'asc'(default) 'desc'
        # internal: default False
        # erc20: default False
        try:
            self.trans = self.api.get_transaction_page(**kargs)
        except client.ClientException as e:
            print(e.message)
        return
    
    def format_trans(self):
        # format value and calculate transaction fee in Ether
        if self.trans == None:
            return print('No transaction data')
        else:
            trans = pd.DataFrame(self.trans)
            trans.gasUsed,trans.gasPrice = trans.gasUsed.astype(int), trans.gasPrice.astype(int)
            trans['TxnFee']= trans.gasPrice * trans.gasUsed / 10 **18
            trans.value = trans.value.astype(str)
            trans.value = trans.value.str.slice(stop = 18)
            trans.value = trans.value.astype(int)
            trans.value = trans.value / 10 ** 16
            trans.timeStamp = pd.to_datetime(trans.timeStamp, unit = 's')
            trans = trans[['blockNumber','timeStamp','from','to','value','TxnFee']]
            trans.to_csv('section1/task3/Transaction.csv', index=0)
            return 

    def get_blocks_mined(self, **kargs):
        # get blocks mined for a single address
        # params: optional
        # page: 
        # offset: default 10000
        # blocktype: 'blocks'(default) 'uncles'
        try:
            self.mined = self.api.get_blocks_mined_page(**kargs)
        except client.ClientException:
            print('No blocks mined')
        return 
    
    def format_mined(self):
        if self.mined == None:
            return print('No mined data')
        else:
            mined = pd.DataFrame(self.mined)
            mined.timeStamp = pd.to_datetime(mined.timeStamp, unit = 's')
            mined.blockReward = mined.blockReward.astype(int) /10 **18
            mined.to_csv('section1/task3/Mined.csv', index=0)
        return


# with open('section1/task3/key.json', mode='r') as file:
#     key = json.loads(file.read())['key']
# address1 = '0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b'
# address2 = '0xddBd2B932c763bA5b1b7AE3B362eac3e8d40121A'
 

# a = Account(address2,key)
# a.get_balance()
# a.add_address(address2)
# a.get_balance_multiple()
# a.get_transaction(offset = 100, sort = 'desc')
# a.format_trans()
# a.get_blocks_mined(offset = 100)
# a.format_mined()