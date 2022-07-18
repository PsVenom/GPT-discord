<div align="center">

# GPT-discord
A discord chatbot powered by Openai's GPT-3, with several other features!

</div>

# So what can the bot do?
- For starters, it can start converstations that feel almost surreal. All of that is thanks to OpenAI's GPT3, a popular large language model
- The bot can also respond to you messages in a Voice Chat by using ffmpeg and Google TTS
- Can perform tts for those awkard moments when you just can't get you microphone to work
  
## Installation

- Run the command to install all the dependencies
  ```
  pip install -r requirements.txt
  ```
- Create an account on [OpenAI](https://openai.com/api/) and generate an API key
- Duplicate & Rename the `.env.example` file to `.env`
- Paste your `bot token` and `openai api key` in the .env file
- Run `bot.py` and the bot should be online
- To enable tts, you'll have to manually install ffmpeg by following [this](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/) tutorial 
- To use a custom GPT-3 engine, edit the variable in line 32 of [main.py](main.py). Replace the existing value with a model name from [here](https://beta.openai.com/docs/models/gpt-3)


