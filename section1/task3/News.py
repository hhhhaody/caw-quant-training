from crypto_news_api import CryptoControlAPI
import pandas as pd
import json

# getLatestRedditPostsByCoin in CryptoControlAPI mistakely gets articles
# getLatestFeedByCoin CryptoControlAPI returns result same as thing with getTopFeedByCoin
# getTopItemsByCoin in CryptoControlAPI returns result same as getTopFeedByCoin
# getLatestItemsByCoin in CryptoControlAPI returns result same as getTopFeedByCoin

class News:
    def __init__(self, api_key):
        self.language = 'en'
        self.api = CryptoControlAPI(api_key)

    def set_language(self, language):
        # English (en default)
        # Chinese/Mandarin 'cn'
        # German 'de'
        # Italian 'it'
        # Japanese 'jp'
        # Korean 'ko'
        # Portuguese 'po'
        # Russian 'ru'
        # Spanish 'es'
        self.language = language

    def getTopNews(self):
        # Get the top news articles.
        self.data, self.formated = None, None
        try:
            self.data = self.api.getTopNews(language=self.language)
            self.formated = self.format_news(self.data)
            print(self.formated)
        except Exception as e:
            print(e)

    def getLatestNews(self):
        # Get the latest news articles.
        self.data, self.formated = None, None
        try:
            self.data = self.api.getLatestNews(language=self.language)  
            self.formated = self.format_news(self.data)
            print(self.formated)
        except Exception as e:
            print(e)

    def getTopNewsByCoin(self, coin):
        # Get the top news articles for a specific coin from the CryptoControl API.
        self.data, self.formated = None, None
        try:
            self.data = self.api.getTopNewsByCoin(coin,language=self.language)
            self.formated = self.format_news(self.data)
            print(self.formated)
        except Exception as e:
            print(e)

    def getTopNewsByCategory(self):
        # Get news articles grouped by category.
        self.data, self.formated = None, None
        try:
            self.data = self.api.getTopNewsByCategory(language=self.language)
        except Exception as e:
            print(e)
            return
        self.formated = pd.concat([self.format_news(self.data[i]) for i in self.data.keys()])
        print(self.formated)


    def getLatestNewsByCoin(self, coin):
        # Get the latest news articles for a specific coin.
        self.data, self.formated = None, None
        try:
            self.data = self.api.getLatestNewsByCoin(coin, language= self.language) 
            self.formated = self.format_news(self.data)
            print(self.formated)
        except Exception as e:
            print(e)

    def getTopNewsByCoinCategory(self, coin):
        # Get news articles grouped by category for a specific coin.
        self.data, self.formated = None, None
        try:
            self.data = self.api.getTopNewsByCoinCategory(coin, language=self.language) 
            self.formated = self.format_news(self.data)
            print(self.formated)
        except Exception as e:
            print(e)

    def getTopTweetsByCoin(self, coin):
        # Get top tweets for a particular coin
        self.tweets, self.formated = None, None
        try:
            self.tweets = self.api.getTopTweetsByCoin(coin,language=self.language)
            self.formated = self.format_tweets(self.tweets)
            print(self.formated)
        except Exception as e:
            print(e)

    def getLatestTweetsByCoin(self, coin):
        # Get latest tweets for a particular coin
        self.tweets, self.formated = None, None
        try:
            self.tweets = self.api.getLatestTweetsByCoin(coin,language=self.language)
            self.formated = self.format_tweets(self.tweets)
            print(self.formated)
        except Exception as e:
            print(e)

    def getTopRedditPostsByCoin(self, coin):
        # Get top reddit posts for a particular coin
        self.reddit, self.formated = None, None
        try:
            self.reddit = self.api.getTopRedditPostsByCoin(coin,language=self.language)
            self.formated = self.format_reddit(self.reddit)
            print(self.formated)
        except Exception as e:
            print(e)

    def getTopFeedByCoin(self, coin):
        # Get a combined feed (reddit/tweets/articles) for a particular coin sort by time
        self.feed, self.formated = None, None
        try:
            self.feed = self.api.getTopFeedByCoin(coin,language=self.language)
            self.formated = self.format_feed(self.feed)
            print(self.formated)
        except Exception as e:
            print(e)    
    
    def getCoinDetails(self, coin):
        try:
            self.coin = self.api.getCoinDetails(coin,language=self.language)
            print(pd.DataFrame.from_dict(self.coin,orient = 'index'))
        except Exception as e:
            print(e)       

    def export_csv(self):
        # export formated data to csv
        self.formated.to_csv('section1/task3/Formated_Data.csv', index = 0)
    
    @staticmethod
    def format_news(data):
        news = pd.DataFrame(data)
        news = news[['primaryCategory', 'coins', 'title', 
            'url', 'source','publishedAt']]
        news['coins'] = [[i['tradingSymbol'] for i in news.coins[j]] for j in range(news.coins.size)]
        news['source'] = [i['name'] for i in news.source]
        return news 
    
    @staticmethod
    def format_tweets(data):
        tweets = pd.DataFrame(data)
        tweets = tweets[['text', 'url', 'publishedAt','retweetCount', 'favoriteCount']]
        return tweets
    @staticmethod
    def format_reddit(data):
        reddit = pd.DataFrame(data)
        reddit = reddit[['title', 'url', 'subreddit', 'publishedAt' , 'comments', 'upvotes']]
        return reddit

    def format_feed(self, data):
        feed = pd.DataFrame(data)
        article = self.format_news([x for x in feed.article.dropna()])
        tweet = self.format_tweets([x for x in feed.tweet.dropna()])
        reddit = self.format_reddit([x for x in feed.reddit.dropna()])
        tweet = tweet.rename(columns={'text':'title'})
        df = pd.concat([article,tweet,reddit]).sort_values('publishedAt',ascending=False)
        df = df.drop('coins', axis = 1)
        # df = df[['title','url','publishedAt']]
        return df

# with open('section1/task3/controlkey.json', mode='r') as file:
#     key = json.loads(file.read())['key']
# api = News(key)
# api.getTopNews()
# api.getLatestNews()
# api.getTopNewsByCoin("bitcoin")
# api.getTopTweetsByCoin("eos")
# api.getTopRedditPostsByCoin("ripple")
# api.getTopFeedByCoin("neo")
# api.export_csv()
# api.getCoinDetails("ethereum")






