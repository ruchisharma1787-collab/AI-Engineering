import os 
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

load_dotenv()

my_api_key = os.getenv("OPEN_ROUTER_API")

client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=my_api_key)

model = "nvidia/nemotron-3.5-lightning:free"

def llm_ans(prompt):
    message = [
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=message
    )
    answer = response.choices[0].message.content
    return answer

bad_prompt = """ #ROLE : you are a customer support assistant at a mobile/laptop company.
# TASK : you have to classify the issue in a category.
# CONSTRAINTS : you have to classify the issue in one of the following categories : technical , billing, return.
# output format : you have to output the category only.
# fallback : if you are not able to classify the issue in any of the above categories then output "not classified".
this is a user complain :
my laptop is not working . iam not happy with it . please refund my money.
classify this """

print(llm_ans(bad_prompt))


