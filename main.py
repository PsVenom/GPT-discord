import random
import openai
import pickle
import os
from bs4 import BeautifulSoup
import urllib
import cv2

openai.api_key = 'ENTER-OPENAI-TOKEN-HERE'
completion = openai.Completion()
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
async def ask(question, model_exist = False, chat_log=None):
    if chat_log is None:
        chat_log = "Human: Hello, who are you? AI: I am an AI created by OpenAI. How can I help you today? "
    prompt = f'{chat_log}Human: {question}\nAI:'
    if os.path.isdir("model.csv"):
       with open("model.csv", "ab") as file:
           a = pickle.load(file)
       ft = openai.FineTune.retrieve(id= a["id"])
       ftm = ft["fine_tuned_model"]

       response = completion.create(model= ftm, prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=70)
    else:
     response = completion.create(prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=70)
     model_exist = True
    answer = response.choices[-1].text.strip()
    return answer


def fit(filepath = 'scratch.json'):
    with open(filepath, "r+") as f:
        response = openai.File.create(file=f, purpose='fine-tune')
    response = openai.FineTune.create(training_file=response["id"], model='davinci' )
    file = open('model.csv', "wb")
    pickle.dump(response, file)
    file.close()

def scraper(url_link = "https://www.google.com/search?q=ahegao&rlz=1C1YQLS_enIN994IN994&sxsrf=ALiCzsYUc788mZWD-tAhRGNmklg8-rrpAw:1652733172219&source=lnms&tbm=isch&sa=X&ved=2ahUKEwifzY3t7uT3AhXEjOYKHXroCx0Q_AUoAXoECAIQAw"):
 a = []
 request = urllib.request.Request(url_link, None, header)  # The assembled request
 response = urllib.request.urlopen(request)
 htmldata = response.read()
 soup = BeautifulSoup(htmldata, 'html.parser')
 images = soup.find_all('img')
 for item in images:
     a.append(item['src'])
 return a[random.randint(0, len(a))]


async def getImg(fp = 'danbooru2020-ahegao-handpicked-cropped'):
    a = list(os.listdir(fp))
    return fp+"/"+a[random.randint(0, len(a))]

