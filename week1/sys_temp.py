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

message = [{"role": "system", "content": "you are a brand manager who suggests name for a new cafe. name should be in one word and only one name "}, {"role": "user", "content": "suggest a name for a new cafe"}]

response = client.chat.completions.create(
    model=models,
    messages=message 
    # temperature= 1,
)
# print(response)

answer = response.choices[0].message.content
print(answer)