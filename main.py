import os
import openai

openai.api_key = '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'
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
