import etherscan.proxies as proxies
import json
import pandas as pd

class Proxy:
    def __init__(self, api_key):
        self.api = proxies.Proxies(api_key= api_key)
        self.block = None
        self.transaction = None
    
    def get_gas_price(self):
        # Returns the current gas price
        price = self.api.gas_price()
        print(int(price, 16)/10**9,end=' ')
        print(' gwei')  
        return

    def get_block_by_number(self, block_number):
        # get block info
        try:
            self.block = self.api.get_block_by_number(block_number)
        except:
            print('Error')
            return
        if self.block == None:
            print('No block data')
        return
    
    def format_block_data(self, trans = False):
        # display block info
        # trans: generate a csv for transaction in the given block
        #        default False
        if self.block == None:
            return print('No block data')
        else:
            block = self.block.copy()
            transactions = block['transactions']
            block['transactions'] = len(transactions)
            list = ['extraData', 'hash', 'logsBloom', 'mixHash', 'nonce', 'parentHash', 'receiptsRoot', 'sha3Uncles', 'stateRoot', 'transactionsRoot']
            [block.pop(x) for x in list]

            list = ['difficulty', 'gasLimit', 'gasUsed', 'number', 'size', 'totalDifficulty']
            for i in list:
                block[i] = int(block[i],16)
            block['timestamp'] = pd.to_datetime(int(block['timestamp'],16), unit = 's')
            print('Block Info\n')
            print(pd.Series(block))
            
            if(len(transactions) != 0 and trans == True):
                transactions = pd.DataFrame(transactions)
                list= ['gas','gasPrice','value']
                for i in list:
                    transactions[i] = transactions[i].apply(int, base=16)
                transactions.value = transactions.value / 10**18
                transactions['TxnFee(Ether)']= transactions.gas * transactions.gasPrice / 10**18
                transactions=transactions[['hash', 'from','to','value','TxnFee(Ether)']]
                transactions.to_csv('section1/task3/Transaction_in_block.csv', index=0)
            elif len(transactions)== 0 and trans == True:
                print('No transactions')

            return

    def get_block_transaction_count_by_number(self, block_number):
        # Returns the number of transactions in a block from a block matching the given block number
        try:
            tx_count = self.api.get_block_transaction_count_by_number(block_number = block_number)
        except:
            print('Error')
            return
        if tx_count == '0x0' or tx_count == None:
            return print('No transaction found')
        else:
            return print(int(tx_count,16))
    
    def get_code(self, contract_address):
        # get the ByteCode of the given contract address
        # to get human readable code use get_sourcecode in contract.py
        try:
            code = self.api.get_code(contract_address)
        except:
            print('Error')
            return
        if code == '0x':
            print('No code found')
        else:
            print(code)
        return

    def get_most_recent_block(self):
        return print(int(self.api.get_most_recent_block(), 16))

    def get_storage_at(self, contract_address, pos):
        # Returns the value from a storage position at a given address
        try:
            value = self.api.get_storage_at(contract_address,pos)
            print(value)
        except:
            print('Error')
        return

    def get_transaction_by_blocknumber_index(self, block_number, index):
        # Returns information about a transaction by block number and transaction index position
        try:
            self.transaction = self.api.get_transaction_by_blocknumber_index(block_number = block_number, index= index)
        except:
            print('Error')
            return
        if self.transaction == None:
            print('No transaction found')
        else:
            print(self.transaction)
        return

    def get_transaction_by_hash(self, hash):
        # Returns the information about a transaction requested by transaction hash
        try:
            self.transaction = self.api.get_transaction_by_hash(tx_hash = hash)
        except:
            print('Error')
            return
        if self.transaction == None:
            print('No transaction found')
        else:
            print(self.transaction)
        return

    def format_transaction_data(self):
        # format the transaction get by index or hash
        if self.transaction == None:
            return print('No transaction data')
        else:
            transaction = self.transaction.copy()
            list= ['gas','gasPrice','value']
            for i in list:
                transaction[i] = int(transaction[i],16)
            transaction['value'] = transaction['value'] / 10**18
            transaction['TxnFee(Ether)']= transaction['gas'] * transaction['gasPrice'] / 10**18
            list = ['blockNumber', 'gas', 'input', 'gasPrice', 'hash', 'nonce', 'transactionIndex', 'v', 'r', 's']
            [transaction.pop(i) for i in list]
            return print(pd.Series(transaction))

    def get_transaction_count(self, address):
        # Returns the number of transactions sent from an address
        try:
            count = self.api.get_transaction_count(address)
            print(int(count,16))
        except:
            print('Error')
        return

    def get_transaction_receipt(self, hash):
        # Returns the receipt of a transaction by transaction hash
        try:
            receipt = self.api.get_transaction_receipt(hash)
        except:
            print('Error')
            return
        print(pd.Series(receipt))
        return

    def get_uncle_by_blocknumber_index(self, block_number, index):
        # Returns information about a uncle by block number
        try:
            uncle = self.api.get_uncle_by_blocknumber_index(block_number= block_number, index = index)
        except:
            print('Error')
            return
        if uncle == None:
            print('No uncle found')
        else:
            print(pd.Series(uncle))
        return
    

with open('section1/task3/key.json', mode='r') as file:
    key = json.loads(file.read())['key']
api = Proxy(key)

# api.get_gas_price()

# api.get_block_by_number(1204325)
# api.format_block_data()

# api.get_block_transaction_count_by_number('0x10FB78')

# contract1 = '0xf75e354c5edc8efed9b59ee9f67a80845ade7d0c'
# contract2 = '0xbcf935d206ca32929e1b887a07ed240f0d8ccd22'
# api.get_code(contract1)
# api.get_code(contract2)

# api.get_most_recent_block()

# api.get_storage_at('0x6e03d9cce9d60f3e9f2597e13cd4c54c55330cfd', 0)

# api.get_transaction_by_blocknumber_index('0x57b2cc',2)
# hash = '0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1'
# api.get_transaction_by_hash(hash)


# api.get_transaction_count('0x6E2446aCfcec11CC4a60f36aFA061a9ba81aF7e0')

# api.get_transaction_receipt('0xb03d4625fd433ad05f036abdc895a1837a7d838ed39f970db69e7d832e41205d')

# api.get_uncle_by_blocknumber_index('0x210A9B',1)

                          

