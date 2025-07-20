import spacy
from collections import Counter
import requests
from dotenv import load_dotenv
load_dotenv()
import os
nlp = spacy.load("en_core_web_sm")
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_TOKEN}",  # Replace with your token
    "Content-Type": "application/json"
}

def extract_keywords(text):
    tokens = nlp(text.lower())
    filterStopwords = [w.text for w in tokens if w.is_alpha and not w.is_stop ]
    freqWords = Counter(filterStopwords)
    cmnWords = [word for word,freq in freqWords.most_common(20)]
    return cmnWords



def refine_resume(resume,jobDesc):
    job_keywords = extract_keywords(jobDesc)
    resume_keywords = extract_keywords(resume)
    missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]
    prompt = {
        "messages": [
        {
            "role": "You are a professional resume editor",
            "content": f"""
            You are a professional resume editor.
            ### Objective:
            Please refine the following resume to:
            1. Naturally incorporate the following target keywords into relevant work experience or summary sections:  
               👉 {', '.join(missing_keywords)}
            2. Ensure the tone is professional, concise, and aligned with the job description below.
            3. Align Professional Summary as per job role.
            4. If there is no changes in any section donot same "Remain same" just add them as it is.
            5. Do NOT keyword-stuff — use each keyword naturally and only where relevant.
            6. Rewrite only where necessary — preserve the candidate’s original achievements and structure.
            7. Give whole resume with new changes as response.
            8. Make sure you send whole resume as output.

            ### Resume:
            {resume}

            ### Job Description:
            {jobDesc}

            ### Refined Resume:
            """
        }
         ],
        "model": "meta-llama/Llama-3.2-3B-Instruct:novita"
            }
    response = requests.post(
            API_URL,
            headers=headers,
            json=prompt
        )
    # print(response.json())
    return response.json()

# def get_missing_keywords(job_description, resume_text):
#     job_keywords = extract_keywords(job_description)
#     resume_keywords = extract_keywords(resume_text)
#     missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]
#     return missing_keywords

# Optional standalone test
if __name__ == '__main__':
    with open('./samples/job_desc.txt', 'r') as j:
        jobDesc = j.read()
    with open('./samples/resume.txt', 'r') as r:
        resume = r.read()
    print(refine_resume(resume,jobDesc))
    jobKeywords = extract_keywords(jobDesc)
    resumeKeywords = extract_keywords(resume)
    missKeywords = [kw for kw in jobKeywords if kw not in resumeKeywords]