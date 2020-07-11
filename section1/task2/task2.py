from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd

class Binance:

    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_candle(self, symbol, interval, start, end='now'):
        # interval: eg:'1d','1h','30m' (str)
        # start: start time (str)
        # end: end time (str)
        #      default to now

        client = Client("", "")
        try:
            klines = client.get_historical_klines(symbol, interval, start, end)
        except BinanceAPIException as e:
            print(e.message)
            return
        self.klines = klines
        return klines

    def format_candle(self):
        df = pd.DataFrame(self.klines)
        df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'BaseAsset Volume', 'Close time', 'QuoteAsset Volume',
                      'Number of trades', 'Taker buy baseAsset volume', 'Taker buy quoteAsset volume', 'Ignore']
        df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
        df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
        closetime = df.pop('Close time')
        df.insert(1, closetime.name, closetime)
        df.pop('Ignore')
        df.to_csv('section1/task2/CandleData.csv', index=0)
        return

    def get_transactions(self, symbol, number=500):
        # number: # of trades wish to check (int)
        #         default:500 max:500
        # most recent trades show first

        client = Client("", "")
        try:
            trades = client.get_recent_trades(symbol=symbol, limit=number)
        except BinanceAPIException as e:
            print(e.message)
            return
        self.trades = trades
        return trades

    def format_trade(self):
        df = pd.DataFrame(self.trades)
        df.pop('id')
        time = df.pop('time')
        df.insert(0, time.name, time)
        df = df.sort_values(by='time', ascending=False)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.to_csv('section1/task2/TradesData.csv', index=0)
        return

    def get_marketdepth(self, symbol, number=100):
        # number: # wish to check (int)
        #         default:100 max:1000

        client = Client("", "")
        try:
            depth = client.get_order_book(symbol=symbol, limit=number)
        except BinanceAPIException as e:
            print(e.message)
            return
        self.depth = depth
        return depth

    def formant_depth(self):
        data = self.depth
        bids, asks = pd.DataFrame(data['bids']), pd.DataFrame(data['asks'])
        bids.columns, asks.columns = ['Bids Price', 'Bids Qty'], ['Ask Price', 'Ask Qty']
        df = pd.concat([bids, asks], axis=1)
        df.to_csv('section1/task2/MarketDepth.csv', index = 0)
        return


    def test_order(self, symbol, action, type, **kwargs):
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

        try:
            self.client.create_test_order(symbol=symbol, side=action, type = type, **kwargs)
        except BinanceAPIException as e:
            print(e.message)
            return

Binance = Binance('','')
Binance.get_candle('BNBBTC','1h','2020-06-01')
Binance.format_candle()

Binance.get_transactions('BTCUSDT')
Binance.format_trade()

Binance.get_marketdepth('BTCUSDT')
Binance.formant_depth()