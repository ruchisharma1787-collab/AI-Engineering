# AI Resume Evaluator

An LLM-powered Resume Evaluator that analyzes resumes against a job description and generates a match score with relevant insights.

## Features

- Extracts text from PDF and DOCX resumes.
- Uses an LLM to structure job descriptions and resume information.
- Evaluates resumes against job requirements.
- Generates a match score out of 100.
- Highlights matched skills, missing required skills, strengths, and improvement areas.
- Ranks resumes based on their match scores.

## Tech Stack

- Python
- OpenAI Python SDK
- OpenRouter API
- Pydantic
- PyPDF
- python-docx

## Project Structure

```text
project/
├── resume_parser.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup and Installation

1. Clone or download this repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your OpenRouter API key using the environment variable name expected by the code.
5. Place your own test resumes in the `resume/` folder.
6. Configure the model name and API settings in the script if needed.
7. Run the project:

```bash
python resume_parser.py
```

## Output

The application parses the job description and resumes, calculates an LLM-generated match score, provides matching insights, and ranks the resumes.

## Important Notes

- Never commit API keys, `.env` files, or private resumes.
- Match scores are AI-generated estimates, not definitive hiring decisions.
- Review the extracted information and evaluation results before using them in recruitment.

## Future Improvements

- Consistent output validation.
- Improved error handling.
- A cleaner evaluation report.
- A user-friendly interface.

## Disclaimer

This project is built for learning and demonstration purposes. It should support, not replace, human review in hiring decisions.