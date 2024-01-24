import json
import os
import pandas as pd
import streamlit as st

import google.generativeai as genai
from datetime import datetime, timedelta


# setup the web page
st.set_page_config(page_title="What's buzzing", layout='wide')

# configure the API key
@st.cache_resource
def configure_genai():
    genai.configure(api_key=st.secrets["gemini_api_key"])    # google gemini

configure_genai()

def get_gemini_response(prompt, user_input):
    """
    Function to get the response of Gemini model

    Args:
        prompt: Prompt of our AI model
        tweet: Tweet text
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], user_input])
    return response.candidates[0].content.parts[0].text

def get_conclusion_prompt(topic):
    conclusion_prompt = [
        f"""
        From a list of themes that belongs to the topic "{topic}", you have to identify the five most common themes with numbering from 1-5, where 1 represent the most common and so on.
        The output should be in the format:
        Number. [theme in bold text]: Its specific verbose info 
        Note:
        - Keep each theme concise and verbose at the same time without exceeding 10-word limit.
        - It doesn't need to be exactly any element from the list, but it should be highly correlated.
        - It should not be the superset topic only, e.g {topic} Trends or {topic}, and must be very specific to that topic.
        """
    ]
    return conclusion_prompt

# Load the topics
with open('topics.json', 'r') as file:
    topics = file.read()

topics = json.loads(topics)

st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

st.markdown("<h2>GenAI App: Find what's buzzing on X(twitter)</h2>", unsafe_allow_html=True)

st.markdown('<h5 style="color: #f5386e">Choose a topic:</h5>', unsafe_allow_html=True)

# Calculate the number of rows needed
n_topics_row = 7
num_rows = len(topics) // n_topics_row + (len(topics) % n_topics_row > 0)

buttons = []
# Create equally spaced buttons for each item
for i in range(num_rows):
    row_topics = topics[i * n_topics_row: (i + 1) * n_topics_row]
    cols = st.columns(n_topics_row)
    
    for col, topic in zip(cols, row_topics):
        buttons.append(col.button(f"#{topic}", use_container_width=True))

content_cols = st.columns([1, 1, 0.85])

# show the info related to tweets
upto_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
info_tweet = st.markdown(f'<div style="text-align: center; padding-top: 8rem"><h5>Choose a topic to know yesterday&apos;s buzz <br><span style="color: #1be3a7">For date: <i>{upto_date}</i></span></h5></div>', unsafe_allow_html=True)

buzz_subheading = None
# Handle button click
for i, button in enumerate(buttons):
    if button:
        info_tweet.empty()
        if buzz_subheading: buzz_subheading.empty()

        selected_topic = topics[i]

        df = pd.read_csv('data/tweets_cleaned.csv')

        # collect all the themes based on the selected topic
        topic_df = df[df['topic'] == topics[i]]

        
        num_tweets = len(topic_df)

        buzz_subheading = content_cols[0].markdown(f'<h4>Buzz in <span style="color: #3de60e">#{selected_topic}</span> is about:</h4>', unsafe_allow_html=True)

        buzz_placeholder = content_cols[0].empty()

        # show the tweets dataframe
        content_cols[1].markdown(f'<h6>Showing 10/{num_tweets} tweets:</h6>', unsafe_allow_html=True)
        content_cols[1].dataframe(topic_df[['username', 'text']].reset_index(drop=True).iloc[:10,:])

        # show the predicted themes
        themes = topic_df['theme'].tolist()
        content_cols[2].markdown(f'<h6>Respective 10/{num_tweets} themes:</h6>', unsafe_allow_html=True)
        content_cols[2].write(themes[:10])

        loading = content_cols[0].markdown(f'<div style="color: #f1f1f1; text-align: center; padding-top: 10rem;"><h5 style="color: #0e47b6;">Finding...</h5></div>', unsafe_allow_html=True)
        while True:
            try:
                response = get_gemini_response(get_conclusion_prompt(topics[i]), str(themes))
                if response: break
            except:
                continue
        loading.empty()

        buzz_placeholder.write(f"{response}<br><br><span style='color: darkgray'>Note: <i>LLM responses may vary a bit</i></span>", unsafe_allow_html=True)
