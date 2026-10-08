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

from pydantic import BaseModel
class Ticket(BaseModel):
    name: str
    email: str
    issue : str

schema = Ticket.model_json_schema()
response_format = { "type": "json_object"}

system_prompt = f"""Extract the personal information from the ticket strictly based on this schema.and give me the json output {schema}"""


message_system = {"role" : "system" , "content"  :system_prompt} 
text = """hello my name is ruchi. i have an issue in iphone which is not working properly.
my address is delhi. my email is abc@gmail.com.
my contact number is 1234567890. please help me to resolve this issue."""
prompt = f"""
This is a customer ticket:
{text}
Extract the personal information from this ticket.
Return only JSON according to the given schema.
"""

message = {"role": "user", "content": prompt}

messages = [message_system , message]
response = client.chat.completions.create(
    model=models,
    messages= messages,
    response_format = response_format,
)
# print(response)

answer = response.choices[0].message.content
print(answer)

import json
raw_json = answer
data_file = json.loads(raw_json)