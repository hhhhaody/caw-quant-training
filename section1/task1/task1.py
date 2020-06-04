import requests
import json
import datetime
import pandas as pd


def histohour(fsym, tsym, start_time, end_time, e):
    fsym, tsym, start_time, end_time, e = 'BTC', 'USDT', '2017-04-01', '2020-04-01', 'binance'
    start = datetime.datetime.strptime(
        start_time, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp()
    end = datetime.datetime.strptime(
        end_time, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp()

    time = end
    dfs = pd.DataFrame()


    while time > start:
        print('ok')
        payload = {'fsym': fsym, 'tsym': tsym,
                'limit': '2000', 'toTs': str(time), 'e': e}
        print('ok')
        # headers = {
        #     'authorization': 'Apikey 40b27c77d564c7be79bbab182177928b1ad652a13e897f7b763d8420be32845f'}
        r = requests.get(
            'https://min-api.cryptocompare.com/data/v2/histohour', params=payload)
        print('ok')
        content_json = json.loads(r.content)
        df = pd.DataFrame(content_json['Data']['Data'])
        dfs = pd.concat([dfs, df], axis=0)
        time = df['time'][0]

    dfs = dfs.sort_values(by='time')
    dfs = dfs.drop(['conversionType', 'conversionSymbol'], axis=1)
    dfs = dfs[dfs['time'] > start]

    time = dfs.pop('time')
    dfs.insert(6, 'Datetime', time)
    dfs.columns = ['Close', 'High', 'Low', 'Open',
                'Volume', 'Base Volume', 'Datetime']

    return dfs

# histohour('BTC','USDT','2017-04-01','2020-04-01','binance')

# payload = {'fsym': fsym, 'tsym': tsym,
#            'limit': '2000', 'toTs': str(time), 'e': e}
# headers = {
#     'authorization': 'Apikey 40b27c77d564c7be79bbab182177928b1ad652a13e897f7b763d8420be32845f'}
# r = requests.get(
#     'https://min-api.cryptocompare.com/data/v2/histohour', params=payload, headers=headers)
# content_json = json.loads(r.content)
# df = pd.DataFrame(content_json['Data']['Data'])
# dfs = pd.concat([dfs, df], axis=0)
# time = df['time'][0]


# dfs.Datetime = dfs.Timestamp.to_pydatetime()
