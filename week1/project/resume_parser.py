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
job_raw_json = response.choices[0].message.content
import json
# print("Job response:", repr(job_raw_json))
job_details = json.loads(job_raw_json)
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

resume_folder = Path("resume")
all_resumes = []


# print(resume_text)

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

resume_schema = Resume.model_json_schema()
# print(resume_schema)
resume_system_prompt = f""" you are an expert HR assistant. Extract the resume details from the resume text into the following JSON structured format: {resume_schema}
IMPORTANT:
Do not return the schema itself.
Fill the schema with actual information from the resume.
If information is missing, do not invent it."""


for file_path in resume_folder.iterdir():
    if file_path.suffix.lower() in [".pdf", ".docx"]:
        resume_text = extract_resume_text(str(file_path))

        response = client.chat.completions.create(
            model=models,
            messages=[
                {"role": "system", "content": resume_system_prompt},
                {"role": "user", "content": resume_text}
            ],
            temperature=0,
            response_format=response_format
        )

        raw_json = response.choices[0].message.content
        resume_data = json.loads(raw_json)
        resume = Resume(**resume_data)

        all_resumes.append(resume)

print("Total resumes parsed:", len(all_resumes))


# part 3 : Matching the resume with the job description and calculating a match score to determine how well the candidate fits the job requirements
class MatchResult(BaseModel):
    score: float
    details: dict
match_schema = MatchResult.model_json_schema()
# print(match_schema)


match_system_prompt = f"""
You are an expert technical recruiter.

Compare the job description with the candidate's resume.

Return a JSON object containing actual evaluation results,
not the schema definition.

The JSON must have:
- score: a number between 0 and 100
- details: an object containing:
  - matched_skills
  - missing_required_skills
  - experience_match
  - qualifications_match
  - strengths
  - improvement_areas

Use this schema to understand the required structure:
{match_schema}

Do not copy the schema into your response.
Do not invent candidate information.
Return only the actual JSON result.
"""



def final_score(job, parsed_resume):
    response = client.chat.completions.create(
        model=models,
        messages=[
            {
                "role": "system",
                "content": match_system_prompt
            },
            {
                "role": "user",
                "content": f"""
JOB DESCRIPTION:
{job.model_dump_json()}

CANDIDATE RESUME:
{parsed_resume.model_dump_json()}

Evaluate this candidate against the job description.
Return the actual score and matching details as JSON.
"""
            }
        ],
        temperature=0,
        response_format=response_format
    )

    raw_json = response.choices[0].message.content
    print("LLM matching response:", repr(raw_json))

    if not raw_json:
        raise ValueError("LLM returned an empty matching response.")

    result_data = json.loads(raw_json)

    if "score" not in result_data or "details" not in result_data:
        raise ValueError(
            f"Unexpected matching response: {result_data}"
        )

    result = MatchResult(**result_data)
    return result



print("\n===== RESUME MATCHING RESULTS =====")

results = []

for index, parsed_resume in enumerate(all_resumes, start=1):
    print(f"\nEvaluating Resume {index}: {parsed_resume.name}")

    result = final_score(job, parsed_resume)

    results.append({
        "name": parsed_resume.name,
        "email": parsed_resume.email,
        "score": result.score,
        "details": result.details
    })

    print(f"Match Score: {result.score}/100")
    print("Matching Details:")

    print(json.dumps(result.details, indent=4))

print("\n===== CANDIDATE RANKING =====")

ranked_results = sorted(
    results,
    key=lambda item: item["score"],
    reverse=True
)

for rank, candidate in enumerate(ranked_results, start=1):
    print(
        f"{rank}. {candidate['name']} - "
        f"{candidate['score']}/100"
    )











        


