from src.tweet_scraper import TweetScraper
from src.clean_and_transform import data_transform, data_clean
from src.theme_predictor import predict_and_update_theme
import pickle
import json
import os
import psutil
import signal

# ANSI escape codes for colors
class Text:
    MAGENTA = '\033[95m'
    GREEN = '\033[92m'
    BLUE = '\033[34m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Function to terminate Python processes on Unix-based systems
def terminate_python_processes():
    for process in psutil.process_iter(['pid', 'name']):
        if 'python' in process.info['name'].lower():
            try:
                os.kill(process.info['pid'], signal.SIGTERM)
            except Exception as e:
                print(f"Error terminating process {process.info['pid']}: {e}")

def step(step_num, desc):
    print(f"{Text.BOLD}{Text.MAGENTA}Step {step_num}: {Text.BLUE}{desc}{Text.END}")

def step_complete():
    print(f"{Text.BOLD}{Text.GREEN}Completed!{Text.END}{Text.END}")

def main():
    # Step 1: Get the tweets
    step(1, "Loading tweets for all the topics")

    # Load the instance from the file
    with open('scraper_instances/saved_instance.pkl', 'rb') as file:
        scraper = pickle.load(file)

    # scrape the tweets for each topic
    tweet_scraper = TweetScraper(scraper, num_tweets=200)
    tweet_scraper.scrape()
    step_complete()
    
    # Step 2: transformation
    step(2, "Started data transformation")
    data_transform()
    step_complete()

    # Step 3: update theme column in data
    step(3, "Predicting and adding themes")
    predict_and_update_theme()
    step_complete()

    # Step 4: clean data
    step(4, "Started data cleaning")
    data_clean()
    step_complete()
    # terminate_python_processes()

if __name__ == "__main__":
    main()