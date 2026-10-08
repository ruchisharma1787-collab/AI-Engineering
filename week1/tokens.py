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
role = "user"

prompt1 = "Hii"
prompt2 = "Explain time travel in detail."
prompt3 = "write a 1000 word eassy on machine learing"

prompts = [prompt1, prompt2, prompt3]
for prompt in prompts:
    message =[{"role": role , "content" : prompt}]
    response = client.chat.completions.create(
    model=models,
    messages=message , max_tokens = 5000 )
    usage = response.usage
    print(f"Prompt: {prompt} --> your tokens: {usage.prompt_tokens}, completion_tokens: {usage.completion_tokens}, total_tokens: {usage.total_tokens} Finish reasons: {response.choices[0].finish_reason}")


# response = client.chat.completions.create(
#     model=models,
#     messages=message 
#     temperature= 1,
# )
# print(response)

# answer = response.choices[0].message.content
# print(answer)