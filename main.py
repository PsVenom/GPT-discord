import random
import openai
import os
from bs4 import BeautifulSoup
import urllib
from dotenv import load_dotenv

#adding OpenAi api key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

#creating api instance
completion = openai.Completion()
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

#Chatbot with custom trained model or a particular engine
start_chat_log = '''Human: Hello, who are you?
AI: I am doing great. How can I help you today?
'''
def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = openai.Completion.create(
        engine="text-davinci-002",
        #model='Enter your custom trained model name here',
        prompt=prompt,
        temperature=0.5,
        #max_tokens=150,
        #top_p=1,
        #frequency_penalty=0,
        #presence_penalty=0.6,
        stop=['\nHuman']
    )
    answer = response.choices[0].text.strip()
    return answer

#url scraping using beautifulsoup
def scraper(url_link = "https://www.google.com/search?q=ahegao&rlz=1C1YQLS_enIN994IN994&sxsrf=ALiCzsYUc788mZWD-tAhRGNmklg8-rrpAw:1652733172219&source=lnms&tbm=isch&sa=X&ved=2ahUKEwifzY3t7uT3AhXEjOYKHXroCx0Q_AUoAXoECAIQAw", remove = 0):
 a = []
 request = urllib.request.Request(url_link, None, header)  # The assembled request
 response = urllib.request.urlopen(request)
 htmldata = response.read()
 soup = BeautifulSoup(htmldata, 'html.parser')
 images = soup.find_all('img')
 for item in images:
     a.append(item['src'])
 try:
    b=a[random.randint(remove, len(a))] 
 except:
    b="Error"
 return b

#uses the ahegao dataset to get images
async def getImg(fp = 'danbooru2020-ahegao-handpicked-cropped'):
    a = list(os.listdir(fp))
    return fp+"/"+a[random.randint(0, len(a))]
