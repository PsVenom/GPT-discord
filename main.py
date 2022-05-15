import openai

openai.api_key = ''
start_sequence = "\nAI:"
restart_sequence = "\nHuman: "
completion = openai.Completion()
start_chat_log = '''Human: Hello, who are you?
AI: I am doing great. How can I help you today?
'''
def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer
def fit(filepath = 'scratch.json'):
    a = ""
    with open(filepath, "r+") as f:
        response = openai.File.create(file=f, purpose='fine-tune')
        a = response["id"]
    a = openai.FineTune.create(training_file= a, model= 'davinci')
    openai.FineTune.retrieve(id= a["id"])

