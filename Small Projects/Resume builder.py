import os
import google.generativeai as genai
from docx import Document
import pdfplumber

# 🔑 Set your Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "AIzaSyALLjiH7A8KrNhpb5wjHElA7SzPcb2dmvs"
genai.configure(api_key=GOOGLE_API_KEY)

# 📄 Read supported file formats
def read_text_from_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    elif ext == '.docx':
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])

    elif ext == '.pdf':
        text = ''
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        return text

    else:
        raise ValueError("Unsupported file format: " + ext)

# 🤖 Generate response using Gemini
def generate_output(job_desc, resume_text):
    prompt = f"""
You are an expert resume writer and interview coach.

Job Description:
\"\"\"{job_desc}\"\"\"

Candidate Resume:
\"\"\"{resume_text}\"\"\"

Tasks:
1. Rewrite and tailor the resume to match the job description.
2. Generate 10 potential interview questions for this role.
3. Help me create a professional resume for [job title] in [industry]. Here's my experience: [paste your experience].
4. "Generate bullet points for my resume based on this job description: [paste job description]. My experience: [paste your details].
5. Optimize my resume for an ATS (Applicant Tracking System) based on this job description: [paste JD].
Tailored Resume Enhancements
6. Rewrite my resume bullets to reflect measurable impact and leadership. Here's the original: [paste bullets].
7. Suggest strong resume action verbs for a [role] in [industry].
8. Can you give me quantifiable bullet points for a [position]? Assume I improved processes, reduced costs, or led teams.
9. Analyze my resume and suggest improvements for clarity, structure, and effectiveness.

Respond with:
===UPDATED RESUME===
<optimized resume>

===INTERVIEW QUESTIONS===
<questions>
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# 💾 Save the outputs
def save_outputs(output):
    parts = output.split("===INTERVIEW QUESTIONS===")
    if len(parts) != 2:
        raise ValueError("Unexpected response format.")

    resume = parts[0].replace("===UPDATED RESUME===", "").strip()
    questions = parts[1].strip()

    with open("updated_resume.txt", "w", encoding='utf-8') as f:
        f.write(resume)

    with open("interview_questions.txt", "w", encoding='utf-8') as f:
        f.write(questions)

# 🚀 Main function
def main():
    print("📂 Resume Optimizer (Gemini)")

    job_path = input("Enter path to Job Description file: ").strip().strip('"')
    resume_path = input("Enter path to Resume file: ").strip().strip('"')

    try:
        job_desc = read_text_from_file(job_path)
        resume_text = read_text_from_file(resume_path)
    except Exception as e:
        print("❌ File read error:", e)
        return

    print("⏳ Processing with Gemini (1.5 Flash)...")

    try:
        output = generate_output(job_desc, resume_text)
        save_outputs(output)
        print("✅ Updated resume saved as 'updated_resume.txt'")
        print("✅ Interview questions saved as 'interview_questions.txt'")
    except Exception as e:
        print("❌ Gemini API error:", e)

if __name__ == "__main__":
    main()
