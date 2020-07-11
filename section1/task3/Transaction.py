import etherscan.transactions as transactions
import etherscan.proxies as proxies
import json

class Transaction:
    def __init__(self, api_key):
        self.api = transactions.Transactions(api_key=api_key)
        self.check = proxies.Proxies(api_key=api_key)

    def get_status(self, tx_hash):
        # Check Contract Execution Status (if there was an error during contract execution)
        # isError":"0" = Pass , isError":"1" = Error during Contract Execution
        try:   #check if tx exist
            self.check.get_transaction_by_hash(tx_hash)
        except:
            print('Tx not exist')
            return
        try:
            status = self.api.get_status(tx_hash)
        except:
            print('Error')
            return
        print(status)
        return
    
    def get_tx_receipt_status(self, tx_hash):
        # Check Transaction Receipt Status (Only applicable for Post Byzantium fork transactions)
        # status: 0 = Fail, 1 = Pass. Will return null/empty value for pre-byzantium fork
        try:   #check if tx exist
            self.check.get_transaction_receipt(tx_hash)
        except:
            print('Receipt not exist')
            return
        try:
            status = self.api.get_tx_receipt_status(tx_hash)
        except:
            print('Error')
            return
        print(status)
        return

# with open('section1/task3/key.json', mode='r') as file:
#     key = json.loads(file.read())['key']
# api = Transaction(key)
# tx_hash1 = '0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a'
# tx_hash2 = '0x513c1ba0bebf66436b5fed86ab668452b7805593c05073eb2d51d3a52f480a76'
# tx_hash3 = '0xb33f1b6a0fc04a55e79011ab4caa14738d28b44285f6313b4a7d0e85c659d98a'
# api.get_status(tx_hash1)
# api.get_status(tx_hash2)
# api.get_status(tx_hash3)
# api.get_tx_receipt_status(tx_hash1)
# api.get_tx_receipt_status(tx_hash2)
# api.get_tx_receipt_status(tx_hash3)





