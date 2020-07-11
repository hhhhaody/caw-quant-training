import etherscan.blocks as blocks
import etherscan.client as client
import json
import pandas as pd

class Block:
    def __init__(self, api_key):
        self.api = blocks.Blocks(api_key=api_key)
        self.reward = None

    def get_block_reward(self, block):
        # find a block's reward with given block number
        try:
            self.reward = self.api.get_block_reward(block)
        except client.ClientException as e:
            print(e.message)
        return

    def format_reward(self):
        if self.reward == None:
            return print('No block data')
        else:
            reward = pd.DataFrame.from_dict(self.reward, orient='index').T
            reward.timeStamp = pd.to_datetime(reward.timeStamp, unit = 's')
            reward.blockReward, reward.uncleInclusionReward = reward.blockReward.astype(int)/10**18, reward.uncleInclusionReward.astype(int)/10**18
            reward.pop('uncles')
            reward = reward.T
            return print(reward)


# with open('section1/task3/key.json', mode='r') as file:
#     key = json.loads(file.read())['key']
# block = 19729873
# b = Block(key)
# b.get_block_reward(block)
# b.format_reward()