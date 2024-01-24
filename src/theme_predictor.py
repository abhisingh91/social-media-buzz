from dotenv import load_dotenv
load_dotenv()           # load all the environment variables

import json
import os
import pandas as pd

import google.generativeai as genai
from openai import OpenAI

# configure the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))    # chatgpt
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))    # google gemini

def get_gemini_response(prompt, user_input):
    """
    Function to get the response of Gemini model

    Args:
        prompt: Prompt of our AI model
        tweet: Tweet text
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], user_input])
    try:
        return response.candidates[0].content.parts[0].text
    except:
        return response.text

def get_chatgpt_response(prompt, tweet_texts):
    messages = [
        {
            'role': 'system',
            'content': prompt[0]
        }
    ]

    messages.append({
        "role": "user",
        "content": str(tweet_texts)
    })

    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    response = completion.choices[0].message.content
    return response

def get_main_prompt(topic):
    main_prompt = [
        f"""
        You are an expert in guessing the theme of a tweet text in at most 5 words. 
        For the given topic "{topic}", you have to analyze the tweet texts and guess the themes. It may be a tool or technology or anything that mostly corresponds to the given topic. 
        For a given input of list of tweet texts, your output should be a python list, and make sure the elements in the list is the same as the input.
        For the elements whose text appears to be an ad/spam, is very unclear, or doesn't seem to be much related to the topic, then keep empty string ("") at those positions in the output list.
        Here is an example for the topic "Artificial Intelligence":
        ["Using The Power Of #Blockchain To Combat #Deepfake Videos  #ArtificialIntelligence #AI #Deepfakes https://liwaiwai.com/2019/11/27/using-the-power-of-blockchain-to-combat-deepfake-videos/ via @liwaiwaicom", "I am good at statistics. Let me handle your assignments, homework and online classes.   DM or text +1(857)399-2684   #College #Dolph #RHOA #TaylorSwift #iTunes #canvas #cengage #blackboard #Rstudio #MicrosoftExcel #pythonprogramming #dataanalysis"]
        Response: ["Blockchain combat Deepfake Videos", ""]
        """
    ]
    return main_prompt

def predict_and_update_theme():
    # Load the topics
    with open('topics.json', 'r') as file:
        topics = file.read()

    topics = json.loads(topics)

    # get the tweets text from the tweets data
    df = pd.read_csv('data/tweets_final.csv')

    responses = []
    for topic in topics:
        topic_df = df[df['topic'] == topic]
        # row in the dataset
        rows = len(topic_df)
        print(f"Topic: {topic}, Number of tweets: {rows}")

        # get a list of tweet texts in chunks of 10 
        chunk_size = 10
        tweet_texts = [topic_df['text'][i:i+chunk_size] for i in range(0, rows, chunk_size)]

        # use gemini to predict the theme of each tweet
        topic_res = []
        for i, txt_batch in enumerate(tweet_texts):
            print(f"Chunk: {i+1}, Tweets: {len(txt_batch)}")
            while True:
                try:
                    response = get_gemini_response(get_main_prompt(topic), str(txt_batch))
                except:
                    continue
                response = response[1:-1].split(', ')
                if len(response) == len(txt_batch): break
            [topic_res.append(r[1:-1]) for r in response]
        responses.append(topic_res)

    # change the data type of theme column to object
    df['theme'] = df['theme'].astype(object)

    for i, topic in enumerate(topics):    
        topic_df = df['topic'] == topic
        df.loc[topic_df, 'theme'] = responses[i]

    # save the updated df 
    df.to_csv('data/tweets_final.csv', index=False)
    print("Added themes in tweets_final.csv")
