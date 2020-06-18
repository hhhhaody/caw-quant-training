from binance.client import Client
from binance.exceptions import BinanceRequestException, BinanceAPIException, BinanceOrderException
import pandas as pd


class Binance:

    @staticmethod
    def get_candle(baseAsset, quoteAsset, interval, start, end='now'):
        # baseAsset: Name of symbol (str)
        # quoteAsset: Name of symbol (str)
        # interval: eg:'1d','1h','30m' (str)
        # start: start time (str)
        # end: end time (str)
        #      default to now

        client = Client("", "")
        symbol = baseAsset+quoteAsset
        try:
            klines = client.get_historical_klines(symbol, interval, start, end)
        except BinanceAPIException as e:
            print(e.message)
            return
        except BinanceRequestException as e:
            print(e.message)
            return
        df = pd.DataFrame(klines)
        df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', baseAsset+' Volume', 'Close time', quoteAsset+' Volume',
                      'Number of trades', 'Taker buy'+baseAsset+' volume', 'Taker buy'+quoteAsset+' volume', 'Ignore']
        df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
        df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
        closetime = df.pop('Close time')
        df.insert(1, closetime.name, closetime)
        df.pop('Ignore')
        df.to_csv('section1/task2/CandleData.csv', index=0)
        return

    @staticmethod
    def get_transactions(baseAsset, quoteAsset, number=500):
        # baseAsset: Name of symbol (str)
        # quoteAsset: Name of symbol (str)
        # number: # of trades wish to check (int)
        #         default:500 max:500
        # most recent trades show first

        client = Client("", "")
        param = baseAsset+quoteAsset
        try:
            trades = client.get_recent_trades(symbol=param, limit=number)
        except BinanceAPIException as e:
            print(e.message)
            return
        except BinanceRequestException as e:
            print(e.message)
            return
        df = pd.DataFrame(trades)
        df.pop('id')
        time = df.pop('time')
        df.insert(0, time.name, time)
        df = df.sort_values(by='time', ascending=False)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df = df.rename(
            {'qty': baseAsset+' Qty', 'quoteQty': quoteAsset+' Qty'}, axis=1)
        df.to_csv('section1/task2/TradesData.csv', index=0)
        return

    @staticmethod
    def get_marketdepth(baseAsset, quoteAsset, number=100):
        # baseAsset: Name of symbol (str)
        # quoteAsset: Name of symbol (str)
        # number: # wish to check (int)
        #         default:100 max:1000

        client = Client("", "")
        param = baseAsset+quoteAsset
        try:
            trades = client.get_order_book(symbol=param, limit=number)
        except BinanceAPIException as e:
            print(e.message)
            return
        except BinanceRequestException as e:
            print(e.message)
            return
        bids, asks = pd.DataFrame(trades['bids']), pd.DataFrame(trades['asks'])
        bids.columns, asks.columns = ['price', 'qty'], ['price', 'qty']
        bids, asks = bids.stack(), asks.stack()
        df = pd.concat([bids, asks], axis=1)
        df.columns = ['bids', 'asks']
        df.to_csv('section1/task2/MarketDepth.csv')
        return

# Binance.get_candle('BNB','BTC','1h','2020-06-01')
# Binance.get_transactions('BTC','USDT')
# Binance.get_marketdepth('BNB','BTC')

    @staticmethod
    def test_order(baseAsset, quoteAsset, action, type, **kwargs):
        # baseAsset: Name of symbol (str)
        # quoteAsset: Name of symbol (str)
        # action: SELL or BUY (str)
        # type: LIMIT, MARKET, STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER (str)
        # timeInForce: GTC, IOC, FOK (str) 
        # quantity: (int)
        # price: (str)
        # quoteOrderQty: (int)
        # newClientOrderId (str) – A unique id for the order. Automatically generated if not sent.
        # icebergQty (decimal) – Used with iceberg orders
        # newOrderRespType (str) – Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        # recvWindow (int) – The number of milliseconds the request is valid for
        # stopPrice: (int)

        # LIMIT	need: timeInForce, quantity, price
        # MARKET need: quantity or quoteOrderQty
        # STOP_LOSS	need: quantity, stopPrice
        # STOP_LOSS_LIMIT need: timeInForce, quantity, price, stopPrice
        # TAKE_PROFIT need: quantity, stopPrice
        # TAKE_PROFIT_LIMIT need: timeInForce, quantity, price, stopPrice
        # LIMIT_MAKER need: quantity, price

        APIkey = 'Eb3UUw08LomMLXspNtExUyBZXfdo1zdbmSAshG5SyBJxkFqczgzv4uPUFhy36xpQ'
        secretkey = 'NWfXZWn8VBithCgMgVLX24deME7Res05lnoRBjKXu1Rg02jlKYYBB5CNSZtF9L6a'
        client = Client(APIkey, secretkey)

        try:
             client.create_test_order(symbol=baseAsset+quoteAsset, side=action, type = type, **kwargs)
        except BinanceRequestException as e:
            print(e.message)
            return
        except BinanceAPIException as e:
            print(e.message)
            return
        except BinanceOrderException as e:
            print(e.message)
            return
