"use client"
import Image from "next/image";
import styles from "./page.module.css";
import { use, useState } from "react";
import axios from 'axios';

export default function Home() {
  const [info, setInfo] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobDescription, setjobDescription] = useState("")
  const [response, setResponse] = useState([])
  const submit_data = async () => {
    if (!selectedFile) {
      alert("No File Selected")
    }
    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("text", jobDescription);

    try {
      const response = await axios.post("https://ai-resume-keyword-matcher.onrender.com/resume_upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      setResponse(response.data)

    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed!");
    }
    if(response){
    alert('Uploaded')
    console.log(response)
  }
  }
  const download=async()=>{
   if (!response) return;
   const fileName = response.filename
   const fileUrl = `http://localhost:8000/uploaded_resumes/${fileName}`;

  // Just open that URL in a new tab or trigger download
   const a = document.createElement("a");
   a.href = fileUrl;
   a.download = fileName; // hint to browser for download name
   document.body.appendChild(a);
   a.click();
   a.remove();
  }
  
  return (
    <div className={styles.page}>
      <div className="titles">
       <span style={{display:'flex', flexDirection:'column', alignItems:'center'}}> <h2>Mistrume </h2><br></br><p style={{color:'grey', fontStyle:'italic'}}>Resume Optimization with Mistral: Improving ATS Compatibility Through LLMs</p></span>
        <button onClick={() => { setInfo(!info) }}>
          <Image alt="info" className="info_icon" src='/info.png' width={25} height={25} />
        </button>
      </div>
      <main className={styles.main}>

        {info ? <p>
          <i>
            This Project compares Job description with your current Resume extracts missing keywords and uses <b>mistaral model</b> to rewrite the resume
            which meets the job description and tries to improve the <b>ATS</b>.
          </i>
        </p> : null}
        <div className="file_upload">
          <div className="jobDesc">
            <textarea
              placeholder="Copy paste the Job Description"
              className="description_text"
              onChange={(e)=>{
                setjobDescription(e.target.value)
              }}
            />

          </div>
          <div className="resume_upload">
            <p style={{ color: 'black' }}><u>Upload Resume</u></p>
            <input
              type="file"
              name="file"
              onChange={async (e) => {
                setSelectedFile(e.target.files[0]);
              }}
            />
          </div>
            <button onClick={submit_data}>Submit</button>
        </div>
        <div className="result_space">
            {response?.choices?.[0]?.message?.content ?<div dangerouslySetInnerHTML={{ __html: response?.choices[0].message.content.replace(/\n/g, '<br/>') }} />:<p><i>Updated Resume</i></p>}
        </div>
      </main>
    </div>
  );
}
