import requests
import json
import datetime
import pandas as pd

class CryptoCompare:

    @staticmethod
    def get_candle(fsym, tsym, start_time, end_time, e, freq):

        if freq[-1] == 'd':
            base_url = 'https://min-api.cryptocompare.com/data/v2/histoday'
        elif freq[-1] == 'h':
            base_url = 'https://min-api.cryptocompare.com/data/v2/histohour'
        elif freq[-1] == 'm':
            base_url = 'https://min-api.cryptocompare.com/data/v2/histominute'

        if len(start_time) > 10:
            format1 = "%Y-%m-%d %H:%M:%S"
        else:
            format1 = "%Y-%m-%d"

        if len(end_time) > 10:
            format2 = "%Y-%m-%d %H:%M:%S"
        else:
            format2 = "%Y-%m-%d"

        start = datetime.datetime.strptime(
            start_time, format1).replace(tzinfo=datetime.timezone.utc).timestamp()
        end = datetime.datetime.strptime(
            end_time, format2).replace(tzinfo=datetime.timezone.utc).timestamp()

        time = end
        dfs = pd.DataFrame()

        while time > start:
            payload = {'fsym': fsym, 'tsym': tsym,
                    'limit': '2000', 'toTs': str(time),'aggregate': int(freq[0]), 'e': e}
            r = requests.get(base_url, params=payload)
            content_json = json.loads(r.content)
            if content_json['Type'] != 100:
                print('Error!')
                print(content_json['Message'])
                return
            df = pd.DataFrame(content_json['Data']['Data'])
            dfs = pd.concat([dfs, df], axis=0)
            time = df['time'][0]

        dfs = dfs.sort_values(by='time')
        dfs = dfs.drop(['conversionType', 'conversionSymbol'], axis=1)
        dfs = dfs[dfs['time'] > start]

        time = dfs.pop('time')
        dfs.insert(6, 'Datetime', time)
        dfs = dfs.rename({'volumefrom':'Volume','volumeto':'Base Volume'}, axis = 1)
        dfs['Datetime'] = pd.to_datetime(dfs['Datetime'],unit = 's')
        dfs.to_csv('section1/task1/histo.csv', index = 0)
        return

    @staticmethod
    def get_top_cap_n(tsym, n):
        payload = {'tsym': tsym, 'limit':n}
        r = requests.get('https://min-api.cryptocompare.com/data/top/mktcapfull', params = payload)
        content_json = json.loads(r.content)
        if content_json['Type'] != 100:
            print('Error!')
            print(content_json['Message'])
            return
        df = pd.DataFrame(content_json['Data'])

        dfs = pd.DataFrame()
        for i in range(len(df['CoinInfo'])):
            _df = pd.DataFrame(df['CoinInfo'][i])
            dfs=pd.concat([dfs, _df],axis = 0)
        dfs.to_csv('section1/task1/Top_cap_n.csv', columns=['Name','FullName'], index = 0)
        return 
    

# CryptoCompare.get_candle('BTC','USDT','2017-04-01','2020-04-01','binance','1h')
# CryptoCompare.get_top_cap_n('USD',20)

