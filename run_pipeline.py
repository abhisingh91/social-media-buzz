from src.tweet_scraper import TweetScraper
from src.clean_and_transform import data_transform, data_clean
from src.theme_predictor import predict_and_update_theme
import pickle
import json

# ANSI escape codes for colors
class Text:
    MAGENTA = '\033[95m'
    GREEN = '\033[92m'
    BLUE = '\033[34m'
    END = '\033[0m'
    BOLD = '\033[1m'

def step_complete():
    print(f"{Text.BOLD}{Text.GREEN}Completed!{Text.END}{Text.END}")

def main():
    # Step 1: Get the tweets
    print(f"{Text.BOLD}{Text.MAGENTA}Step 1: {Text.BLUE}Loading tweets for all the topics{Text.END}")

    # Load the instance from the file
    with open('scraper_instances/saved_instance.pkl', 'rb') as file:
        scraper = pickle.load(file)

    # scrape the tweets for each topic
    tweet_scraper = TweetScraper(scraper, num_tweets=30, until=5)
    tweet_scraper.scrape()
    step_complete()
    
    # Step 2: transformation
    print(f"{Text.BOLD}{Text.MAGENTA}Step 2: {Text.BLUE}Started data transformation{Text.END}")
    data_transform()
    step_complete()

    # Step 3: update theme column in data
    print(f"{Text.BOLD}{Text.MAGENTA}Step 3: {Text.BLUE}Predicting and adding themes{Text.END}")
    predict_and_update_theme()
    step_complete()

    # Step 2: clean data
    print(f"{Text.BOLD}{Text.MAGENTA}Step 4: {Text.BLUE}Started data cleaning{Text.END}")
    data_clean()
    step_complete()

if __name__ == "__main__":
    main()