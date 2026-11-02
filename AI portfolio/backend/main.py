from fastapi import FastAPI
from pathlib import Path
from pypdf import PdfReader
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import json
app = FastAPI()
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API"))

models  = "nvidia/nemotron-3.5-lightning:free"
# pdf extraction
def read_pdf(file_path:Path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text() 
        if page_text:
            text += page_text + "\n"
    return text


# Resume Parser

class Experience(BaseModel):
    company: str
    role: str
    duration: str
    description: str
    skills_used: list[str]


class Resume(BaseModel):
    name: str
    email: str
    phone: str
    total_exp_years: float
    skills: list[str]
    experiences: list[Experience]
class ChatRequest(BaseModel):
    question : str
def ask_candidate(question:str, resume:Resume):
    system_prompt = f"""
    You are an AI assistant representing a candidate. Answer the following question based on the candidate's resume details: {resume.model_dump_json(indent=2)}
    Rules:
    1. answer only using the information from the resume.
    2. never hallucinate or invent information.
    3. if the answer is not present in the resume, respond with "I don't know."
    4.Be professional and concise in your response.
    5. Answer as if HR is asking you in an interview.
     """
    response = client.chat.completions.create(
        model=models,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0
    )
    return response.choices[0].message.content

resume_schema = Resume.model_json_schema()

resume_system_prompt = f"""
You are an expert HR assistant.
Extract the resume details from the resume text into the following JSON structured format: {resume_schema}

IMPORTANT:
Do not return the schema itself.
Fill the schema with actual information from the resume.
If information is missing, do not invent it.
"""


# Parse Single Resume
def parse_resume(resume_text):
    BASE_DIR = Path(__file__).resolve().parent
    resume_path = BASE_DIR / "resume.pdf"

    resume_text = read_pdf(resume_path)

    response = client.chat.completions.create(
    model=models,
    messages=[
        {"role": "system", "content": resume_system_prompt},
        {"role": "user", "content": resume_text}
    ],
    temperature=0
    )

    raw_json = response.choices[0].message.content
    resume_data = json.loads(raw_json)
    resume = Resume(**resume_data)

    print(resume)
    return resume


@app.get("/")
def home():
    
    resume_text = read_pdf(Path("resume.pdf"))
    resume = parse_resume(resume_text)
    print(resume.model_dump_json(indent=2))
    return {
        "message": " Resume parsed!"
    
    }
@app.post("/chat")
def chat(request: ChatRequest):
    resume_text = read_pdf(Path("resume.pdf"))
    resume = parse_resume(resume_text)
    answer = ask_candidate(request.question, resume)
    return {
        "answer": answer
    }

