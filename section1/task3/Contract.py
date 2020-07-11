import etherscan.contracts as contracts
import etherscan.client as client
import json
import pandas as pd

class Contract:
    def __init__(self, address, api_key):
        self.api = contracts.Contract(address=address, api_key=api_key)

    def get_abi(self):
        try:
            abi = self.api.get_abi()
        except client.ClientException as e:
            print(e.message)
            return
        abi = json.loads(abi)
        abi = pd.DataFrame(abi)
        return print(abi)

    def get_sourcecode(self):
        sourcecode = self.api.get_sourcecode()
        sourcecode = sourcecode[0]['SourceCode']
        if sourcecode == '':
            return print('No sourcecode found')
        else:
            i=0
            while i<len(sourcecode):
                for j in range(i, len(sourcecode)):
                    if sourcecode[j] in '\r\n':
                        print(sourcecode[i:j])
                        break
                i = j+2
            return 



# with open('section1/task3/key.json', mode='r') as file:
#     key = json.loads(file.read())['key']
# address = '0xfb6916095ca1df60bb79ce92ce3ea74c37c5d359'
# address1 = '0xddBd2B932c763bA5b1b7AE3B362eac3e8d40121A'

# c = Contract(address1,key)
# c.get_abi()
# c.get_sourcecode()