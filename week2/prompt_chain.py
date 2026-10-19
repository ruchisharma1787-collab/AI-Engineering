import os 
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from time import sleep
load_dotenv()

my_api_key = os.getenv("OPEN_ROUTER_API")
if not my_api_key:
    raise ValueError("OPEN_ROUTER_API environment variable is not set.")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API"))

models  = "nvidia/nemotron-3.5-lightning:free"

JD = """ We are hiring python backend developer.
Requirements:
- Strong python 
- Fastapi or Django
- postgreSQL
- Docker
- AWS 
- REST API
- 2+ yrs of experience """

RESUME = """ 
Name : rahul sharma 
Experience : 3 years as a software developer.
Skills : Python , MYSQL , Fastapi , Docker, Restapi , git .
Projects : built a food delivery backend using Fastapi and Mysql . 
Deployed applications using Docker."""

def ask_llm(system_prompt , user_prompt):
    sys_msg = {"role" : "system"
               ,"content": system_prompt}
    user_msg = {"role": "user"
                , "content": user_prompt}
    messages = [sys_msg , user_msg]
    response = client.chat.completions.create(model = models , messages = messages)
    answer = response.choices[0].message.content
    return answer

def step1_res_ex(RESUME):
    print("STEP 1")
    system_prompt="""
    You are professional HR assistant.Extract the skills from the candidates resume provided. 
    only retrun the skills not other information . do not invent the skills by yourslef ."""

    user_prompt =f"""
    Extract the skills from this resume.
    {RESUME}"""
    return ask_llm(system_prompt, user_prompt)

def step2_JD_extact(JD):
    print("STEP 2")
    system_prompt="""
    You are professional HR assistant.Extract the skills from the Job Description provided. 
    only retrun the skills not other information . do not invent the skills by yourslef ."""

    user_prompt =f"""
    Extract the skills from this Job Description .
    {JD}"""
    return ask_llm(system_prompt, user_prompt)

def step3_match(candidate, jd):
    print("STEP 3")
    system_prompt="""
    You are professional HR assistant.compare the skills of the candidate and the skills required in the JD and produce the final score 
    between 1 and 100. also produce a short verdict whether the candidate is fit for the role."""

    user_prompt =f"""
    Compare and match the skills . 
    JD {jd}
    Candidate {candidate}
    """
    return ask_llm(system_prompt, user_prompt)

candidate = step1_res_ex(RESUME)
print(candidate)
sleep(2)
jd = step2_JD_extact(JD)
sleep(2)
score = step3_match(candidate, jd)
print(score)


