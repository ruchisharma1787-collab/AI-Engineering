import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from pathlib import Path
from pypdf import PdfReader
from docx import Document

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API"))

models  = "nvidia/nemotron-3.5-lightning:free"

#  JOB DESCRIPTION

job_description = """
Job Title: Software Development Engineer (SDE-I)
Company: Amazon
Location: Bengaluru, India

Job Description:
Amazon is looking for passionate Software Development Engineers
to design, develop, and maintain scalable software applications.
The ideal candidate should have strong programming and
problem-solving skills.

Key Responsibilities:
- Design and develop scalable software solutions.
- Write clean, efficient, and maintainable code.
- Work with cross-functional teams to build new features.
- Debug software issues and improve application performance.
- Participate in software design and code reviews.
- Develop reliable systems that can handle large amounts of data.
- Test applications to ensure quality and reliability.

Basic Qualifications:
- Bachelor's degree in Computer Science, Computer Engineering,
  or a related technical field, or currently pursuing the degree.
- Knowledge of at least one programming language:
  Python, Java, or C++.
- Understanding of Data Structures and Algorithms.
- Knowledge of Object-Oriented Programming (OOP).
- Strong analytical and problem-solving skills.
- Understanding of algorithm complexity and software design.

Preferred Qualifications:
- Previous internship or software development project experience.
- Familiarity with relational databases and SQL.
- Knowledge of distributed systems.
- Experience with version control tools such as Git.
- Good communication and teamwork skills.

Expected Skills:
- Python
- Java or C++
- Data Structures and Algorithms
- Object-Oriented Programming
- Problem Solving
- Database Fundamentals
- Software Development
- Debugging and Testing
"""
# part 1: Extracting job details from the job description using pydantic in json format
class JobDetails(BaseModel):
    role : str
    required_skills: list[str]
    preferred_skills: list[str] 
    minimum_experience: float | None
    responsibilities: list[str]
    qualifications: list[str]

job_schema = JobDetails.model_json_schema()
system_prompt = f""" you are an expert HR assistant. Extract the job details from the job description into the following JSON structured format: {job_schema}
IMPORTANT: 
do not return the schema itself. 
Fill the schema with actual information from the job description.
If minimum experience is not mentioned, return null.
If preferred skills are not mentioned, return null.
Do not invent information ."""

response_format = {
    "type": "json_object"
}
messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": job_description
        }
    ]
response = client.chat.completions.create(
    model=models, messages = messages, response_format=response_format)
answer = response.choices[0].message.content
raw_json = answer
# print(raw_json)

import json 
job_details = json.loads(raw_json)
job = JobDetails(**job_details)
# print(job.minimum_experience)
# print(job.required_skills)

# part 2 :extracting text from resume files and parsing them to extract relevant information

def extract_resume_text(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        reader = PdfReader(str(path))
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    elif suffix == ".docx":
        document = Document(str(path))
        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")

resume_path = Path("resume/sample_software_developer_resume.pdf")

resume_text = extract_resume_text(str(resume_path))

print(resume_text)

        


