import os 
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

my_api_key = os.getenv("OPEN_ROUTER_API")
if not my_api_key:
    raise ValueError("OPEN_ROUTER_API environment variable is not set.")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API"))

models  = "nvidia/nemotron-3.5-lightning:free"

prompt = "explain AI Engineering?"
messages = [{"role": "user",
             "content": prompt}]
# response = client.chat.completions.create(model=models, messages= messages)
# # print(response)
# answer = response.choices[0].message.content
# print(answer)

stream = client.chat.completions.create(model=models , messages=messages,
                stream = True)

for chunk in stream:
    content = chunk.choices[0].delta.content 
    if content:
        print(content, end="",
              flush =True)