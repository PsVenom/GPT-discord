import random
import openai
import pickle
import os
from bs4 import BeautifulSoup
import urllib
import cv2
#adding api key
openai.api_key = '<key>'
#creating api instance
completion = openai.Completion()

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "
start_chat_log = '''Human: Hello, who are you?
AI: I am doing great. How can I help you today?
'''
# this is meant for the scraper (experimental)
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
#vanilla chatbot, shorter and more natural
'''
def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = "Human: Hello, who are you? AI: I am an AI created by OpenAI. How can I help you today? "
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = openai.Completion.create(
        engine="text-davinci-002",
        model="curie:ft-personal-2022-05-30-14-47-09",
        prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: My cock is throbbing, what do I do?\nAI: If you're experiencing arousal, you could masturbate or have sex with a consenting partner.\nHuman: I am pretty damn sad, what do I do?\n\nAI:\n\nThere are many things you can do if you're feeling sad. Some people might find comfort in talking to friends or family, while others might prefer to distraction themselves with activities they enjoy. Some other possible options include listening to music, reading, or spending time outdoors.\nHuman: ",
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    answer = response.choices[0].text.strip()
    return answer
'''
def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        #model='ada:ft-personal-2022-05-23-05-34-54',
        model='curie:ft-personal-2022-05-30-14-47-09',
        prompt=prompt, stop=['\nHuman'], temperature=0.5)
    answer = response.choices[0].text.strip()
    return answer

#experimental, uses url scraping using beautifulsoup, if you want to integrate it
def scraper(url_link, remove = 0):
 a = []
 request = urllib.request.Request(url_link, None, header)  # The assembled request
 response = urllib.request.urlopen(request)
 htmldata = response.read()
 soup = BeautifulSoup(htmldata, 'html.parser')
 images = soup.find_all('img')
 for item in images:
     a.append(item['src'])
 return a[random.randint(remove, len(a))]




