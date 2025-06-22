# AI Resume Keyword Matcher & Refiner

This is a simple Python project that helps you improve your resume by analyzing a job description and identifying important keywords missing from your resume. It then uses a local large language model (LLM) via Ollama to rewrite your resume naturally, incorporating those missing keywords to better match the job requirements.

## Features

- Extracts and ranks keywords from the job description and resume using spaCy  
- Finds missing keywords your resume lacks  
- Refines your resume with an AI model (e.g., `mistral`) to integrate missing keywords professionally  
- Avoids keyword stuffing and preserves your original resume’s meaning

## Setup

1. Install dependencies:
```
pip install spacy ollama
python -m spacy download en_core_web_sm
```

2. ollama pull mistral

## Usage
```
python main.py
```
