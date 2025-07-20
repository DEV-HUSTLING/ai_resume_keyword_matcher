from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile,HTTPException,Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
import base64
from fastapi.responses import FileResponse

UPLOAD_DIR = Path("uploaded_resumes")  # Local folder to store uploads
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist
from ai.processing import refine_resume
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
 return {"greeting":"Hello world"}
@app.post("/resume_upload")
async def resume_upload( text: str = Form(...) , file: UploadFile = File(...)):  
    try:
        contents = await file.read()
        encoded_contents = (contents).decode("utf-8")
        
        file_name = os.path.basename(file.filename)
        base_name, _ = os.path.splitext(file_name)
        save_path = UPLOAD_DIR / f"{base_name}.txt"
        # missing_kw = get_missing_keywords(text, encoded_contents)
        refined = refine_resume(encoded_contents, text)

        return refined["choices"][0]["message"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
