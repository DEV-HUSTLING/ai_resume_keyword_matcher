import spacy
from collections import Counter
import ollama

nlp = spacy.load("en_core_web_sm")

# Loading the description and resume text files
with open('job_desc.txt','r') as j:
    jobDesc = j.read()
with open('resume.txt','r') as r:
    resume = r.read()

def extract_keywords(text):
    tokens = nlp(text.lower())
    filterStopwords = [w.text for w in tokens if w.is_alpha and not w.is_stop ]
    freqWords = Counter(filterStopwords)
    cmnWords = [word for word,freq in freqWords.most_common(20)]
    return cmnWords



def refine_resume(keywords):
        print(keywords)
        prompt = f"""
You are a professional resume editor.

### Objective:
Please refine the following resume to:
1. Naturally incorporate the following target keywords into relevant work experience or summary sections:  
   👉 {', '.join(keywords)}
2. Ensure the tone is professional, concise, and aligned with the job description below.
3. Do NOT keyword-stuff — use each keyword naturally and only where relevant.
4. Rewrite only where necessary — preserve the candidate’s original achievements and structure.

### Resume:
{resume}

### Job Description:
{jobDesc}

### Refined Resume:
(Provide the improved version below.)
"""
        
        response = ollama.chat(
             model= 'mistral',
             messages=[
                  {
                       'role':'user',
                       'content': prompt
                  }
             ]
        )
        return response['message']['content']

if __name__ == '__main__':
    jobKeywords = extract_keywords(jobDesc)
    resumeKeywords = extract_keywords(resume)
    missKeywords = [kw for kw in jobKeywords if kw not in resumeKeywords]
    print(missKeywords)
    print(refine_resume(missKeywords))