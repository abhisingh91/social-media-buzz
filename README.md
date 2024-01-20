# GenAI App: Find what's buzzing on Social Media
**This app is deployed on streamlit: https://x-trends.streamlit.app/**


## 📖 About
This app uses the Google **Gemini LLM** Model to tell you the five most buzz themes in any particular topic from **yesterday's** tweets. 
It scrapes data for all the topics as listed in `topics.json`, and it can be changed as per the needs.

## 1. Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/abhisingh91/social-media-trends.git
   ```
2. Navigate to the project folder:
   ```bash
   cd social-media-trends
   ```
3. Install dependencies:
   ```bash
   pip install  -r requirements.txt 
   ```

## 2. Setup Gemini API
1. Create a file `.env` in the root dir of your project:
   ```
   GEMINI_API_KEY=xxxx
   OPENAI_API_KEY=xxxx
   ```
   > **Note:** You may leave OPENAI_API_KEY as xxxx if you don't want to use OpenAI gpt model
2. Create a folder `.streamlit` in the root dir and create a file `secrets.toml` within that
  ```
  gemini_api_key = "xxxx"
  ```
  > **Note:** Use the same API key as in .env and keep it within "".

## 3. Run the pipeline
  ```bash
  python run_pipeline.py
  ```
  This will fetch and store raw, final, and cleaned data of tweets and will apply some steps to make it ready to use.

## 4. Run the streamlit app
   ```bash
   streamlit run app.py
   ```

## 5. Perform EDA on the tweets
   Within the notebooks folder, run the jupyter notebook `data_insights.ipynb` for tweet analysis.

## 🤝 Contributions
I welcome contributions from the community! Whether you want to report a bug, suggest a feature, or contribute code, here's how you can get involved:
  - **🐛 Found a Bug?**<br>
  If you find a bug or unexpected behavior, please [open an issue](https://github.com/abhisingh91/social-media-trends/issues). Make sure to include a detailed description of the issue, steps to reproduce it, and any relevant screenshots.
  
  - **💡 Suggesting Enhancements**<br>
  Fork the repository and create a pull request.


## 🎉 Show Your Support

If you find the project helpful, consider giving it a ⭐️!

### Thank you 🙌


