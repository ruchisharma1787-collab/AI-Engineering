import os 
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import re 
from time import sleep

load_dotenv()
my_api_key = os.getenv("OPEN_ROUTER_API")
if not my_api_key:
    raise ValueError("OPEN_ROUTER_API environment variable is not set.")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API"))

models  = "nvidia/nemotron-3.5-lightning:free"

def get_product_price(product):
    if product == "iphone 17":
        return 90000
    elif product == "iphone 18":
        return 120000
    else:
        return 0 
def calculator(expression):
    try:
        result = eval(expression)
        return result
    except:
        return "Error: Invalid expression"
tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}
system_prompt = """
you are a shoping assistant . 
you have access to the following tools :
get_product_price(product)
calculator(expression)
IMPORTANT :
call tools exactly like this :
Action : get_product_price("iphone 17")
Action : calculator("5000 -343")

never write :
get_product_price(" product = iphone 17") 
calculator(expression="5000 -343")
Follow these rules:
1. Decide what you need to do next.
2. call only one tool at a time.
3. wait until you recieve an observation.
4. after writing an Action , stop immediately and wait for the observation.
5. never guess or invent a tool result.
6. then use the observation to decide what to do next.
7. when the task is complete, give the final amswer

Format :
Thought : what you need to do 
Action : tool_name(argument)

when finished:
Final Answer : your answer
"""

def run_agent(question):
    messages = [
        {
        "role":"system",
        "content" : system_prompt
    }, 
    { 
        "role": "user",
     "content" : question
    }]
    for step in range(5):
        print("\n-----------------")
        print("STEP ", step +1)
        print("-----------------")

        response = client.chat.completions.create(
            model = models,
            messages = messages,
            temperature = 0
        )
        answer = response.choices[0].message.content
        print(answer)

        if "Final Answer" in answer:
            break

        match = re.search(
            r"Action:\s*(\w+)\((.*?)\)",
            answer
        )
        if match:
            tool_name = match.group(1)
            tool_input = match.group(2).strip()
            tool_input = tool_input.strip('"').strip("'")

            if tool_name in tools:
                tool = tools[tool_name]
                observation = tool(tool_input)
            else:
                observation = "Tool not found"

            print(
                "Observation:",
                observation
            )
            messages.append({
                "role": "assistant",
                "content" : answer
            })
            messages.append({
                "role": "user",
                "content" : "Observation:" + str(observation)
            })
            sleep(5)

prompt ="""i have 500000 rupees . what is the price of an iphone17? and how much money will ihave left?"""
run_agent(prompt)



     



