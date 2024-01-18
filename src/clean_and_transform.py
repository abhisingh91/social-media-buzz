import pandas as pd
import warnings

warnings.filterwarnings("ignore")

def data_transform():
    df = pd.read_csv('data/tweets_raw.csv')

    # format the date
    df['date'] = df['date'].str[:12] + df['date'].str[14:]

    df['date_time'] = pd.to_datetime(df['date'], utc=True)

    # split date and time into separate fields
    df['date'] = df['date_time'].dt.date
    df['time'] = df['date_time'].dt.strftime('%H:%M')

    # drop the date_time column
    df.drop('date_time', axis=1, inplace=True)

    # create theme column with empty values
    df['theme'] = ""

    # order the new dataframe
    df = df[['profile_id', 'name', 'username', 'topic', 'text', 'date', 'time', 'likes', 'comments', 'reposts', 'theme']]

    # drop duplicate rows
    df.drop_duplicates(inplace=True)

    # export to csv file
    df.to_csv('data/tweets_final.csv', index=False)

def data_clean():
    df = pd.read_csv('data/tweets_final.csv')

    # drop the rows with irrelevant themes
    df.dropna(subset=['theme'], inplace=True)

    # save the cleaned data
    df.to_csv('data/tweets_cleaned.csv', index=False)