import etherscan.tokens as tokens
import json
import requests as r

class Token:
    def __init__(self, contract_address, api_key):
        self.api_key = api_key
        self.contract_address = contract_address
        self.api = tokens.Tokens(contract_address=contract_address, api_key=api_key)

    def change_token_contract(self, contract_address):
        self.contract_address = contract_address
        self.api = tokens.Tokens(contract_address=contract_address, api_key=self.api_key)

    def get_token_digit(self):
        # use another api to get the token digit
        base_url = 'https://api.ethplorer.io/getTokenInfo/'
        suffix = '?apiKey=freekey'
        result = r.get(base_url+self.contract_address+suffix)
        content = json.loads(result.content)
        return int(content['decimals'])

    def get_token_balance(self, address):
        # get the balance of the token defined by the contract at given account address 
        try:
            balance = self.api.get_token_balance(address=address)
            digit = self.get_token_digit()
            print(int(balance)/10**digit)
        except:
            print('Error')
        return

    def get_total_supply(self):
        # get total supply of the token defined by the contract
        try:
            supply = self.api.get_total_supply()
            digit = self.get_token_digit()
            print(int(supply)/10**digit)
        except:
            print('Error')
        return


# with open('section1/task3/key.json', mode='r') as file:
#     key = json.loads(file.read())['key']
# contract_address = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'
# api = Token(contract_address, key)
# address = '0xe04f27eb70e025b78871a2ad7eabe85e61212761'
# api.get_token_balance(address)
# api.get_total_supply()
