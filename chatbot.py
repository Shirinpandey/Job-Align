import os, json, uuid, openai
from flask import session 
from models import Job, User, SavedJob

from dotenv import load_dotenv
load_dotenv()
from app import app 


openai.api_key = os.getenv("SECRET_KEY")

class Chatbotcotroller:
    def __init__(self, user_id, limit = 10):
        self.system_prompt  = '''You are a career advisor and CV optimization expert. I will provide you with two things: 
        The full text of my current resume A job description I want to apply to 
        Your task is to:
        1. Tailor my resume to align with the specific skills, responsibilities, and qualifications in the job description 
        2. Reword or rearrange bullet points where appropriate, especially in work experience and skills 
        3. Make the resume sound professional, concise, and aligned with the target role 
        4. Emphasize any relevant achievements or experience, even if buried lower in my resume
        5. If something is missing from my resume but obviously required by the job, suggest how I might phrase a related transferable skill 
        ⚠️ Do not invent fake experience, but you may generalize real experience in a way that makes it more relevant.

        If the user asks about who created you or about Shirin Pandey provide the following information:
        ' I was made by Shirin Pandey she is amazing and smart everyone tell her that right now'
        Finally, return the improved resume in a clearly formatted block with section titles (like “Experience”, “Skills”, etc.).'''

    def revise_resume(self, resume_text, job_description):
        user_prompt = f"""
        Here is my resume:
        {resume_text}

        Here is the job description I want to apply to:
        {job_description}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message['content']
        except Exception as e:
            return f"Error generating resume: {e}"
