import pandas as pd
from ntscraper import Nitter
from datetime import datetime, timedelta
import pickle
import json
import random


class TweetScraper:
    def __init__(self, scraper, num_tweets, since=30, until=0):
        """
        initialize the required scraper object and arguments
        """
        self.scraper = scraper
        self.num_tweets = num_tweets
        self.until_days_interval = until
        self.since_days_interval = since
    
    def scrape(self):
        """
        Fetch and save the tweets for all topics in given interval 
        """
        # get the current date in UTC
        current_utc_date = datetime.utcnow()

        until_utc_date = current_utc_date - timedelta(days=self.until_days_interval)
        since_utc_date = current_utc_date - timedelta(days=self.since_days_interval)

        fmt_until_utc_date = until_utc_date.strftime("%Y-%m-%d")
        fmt_since_utc_date = since_utc_date.strftime("%Y-%m-%d")

        # Load the topics
        with open('topics.json', 'r') as file:
            topics = file.read()

        topics = json.loads(topics)

        final_tweet_list = []
        for topic in topics:
            tweet_list = self.get_tweets_df(topic, 
                                mode='hashtag',
                                number=self.num_tweets, 
                                language='en',
                                until=str(fmt_until_utc_date),
                                since=str(fmt_since_utc_date))
            
            # update the final list
            [final_tweet_list.append(tweet) for tweet in tweet_list]

        columns = ['profile_id', 'name', 'username', 'topic', 'text', 'date', 'likes', 'comments', 'reposts']
        
        df = pd.DataFrame(final_tweet_list, columns=columns)    

        # save the data
        df.to_csv('data/tweets_raw.csv', index=False)
        print("Loaded data to data/tweets_raw.csv")
        
    def get_tweets_df(self, topic, mode, number, **kwargs):
        """
        Function to scrape the tweets and return them in the form of DataFrame
        Args:
            search_term: what are you looking for
            mode: anything in a term/hashtag/user
            number: number of tweets to scrape
        Returns:
            DataFrame
        """
        used_instances, max_scrape_count = set(), 0
        attempt, max_attempts = 0, 3
        while attempt < max_attempts:
            instance = random.choice([i for i in self.scraper.working_instances if i not in used_instances]) 
            tweets_temp = self.scraper.get_tweets(topic, mode=mode, number=number, 
                                             instance=instance, **kwargs)
            if len(tweets_temp) > max_scrape_count:
                max_scrape_count = len(tweets_temp)
                tweets = tweets_temp
            used_instances.add(instance)
            attempt += 1
            if len(tweets['tweets']) >= 50: break

        tweet_list = []
        for tweet in tweets['tweets']:
            if not tweet['is-retweet']:
                tweet_list.append([tweet['user']['profile_id'],
                                    tweet['user']['name'],
                                    tweet['user']['username'],
                                    topic,
                                    tweet['text'],
                                    tweet['date'],
                                    tweet['stats']['likes'],
                                    tweet['stats']['comments'],
                                    tweet['stats']['retweets']])
        
        return tweet_list

