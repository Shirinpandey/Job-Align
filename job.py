from flask import Blueprint
from flask import Flask, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge
import PyPDF2
import os,nltk, json
from io import BytesIO
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
import spacy, requests, json
from flask import current_app
from models import Job
from auth import current_user
from extension import db 


nlp = spacy.load("en_core_web_md")

job =  Blueprint('job',__name__)

@job.route('/', methods = ['GET','POST'])
def upload():
    try:
        file = request.files['cv']
        if not file:
            return "No file uploaded"
        contents = cv_reading(file)

        from models import CV

        new_cv = CV(user_id = current_user.id if current_user else None, content= contents)
        db.session.add(new_cv)
        db.session.commit()
        
        new_file = storefiles()
        cleaned_cv = clean_data(contents)
        cv_doc = nlp(cleaned_cv)
        similarity_doc = []
        
        for job in new_file:
            cleaned_file = clean_data(job['description'])
            job_doc = nlp(cleaned_file)
            similarity = cv_doc.similarity(job_doc)
            similarity_doc.append((job,similarity))
        
        similarity_doc.sort(key = lambda x:x[1],reverse= True)
        return render_template('results.html', job_listing = similarity_doc, new_list = new_file )
    except RequestEntityTooLarge:
        return "File is larger than 16 MB"
    

def storefiles():
    with open(os.path.join("jobs", "job.json"), 'r') as f:
        jobs = json.load(f)

    return jobs 


def clean_data(jobs):
    lower_jobs = jobs.lower()
    cleaned_char = []
    for char in lower_jobs:
        if char.isalnum() or char.isspace():
            cleaned_char.append(char)
    cleaned_data = ''.join(cleaned_char)
    cleaned_no_space = ' '.join(cleaned_data.split())

    stops = set(stopwords.words('english'))
    word = cleaned_no_space.split()
    filtered_words = [w for w in word if w not in stops]

    return ' '.join(filtered_words)


def cv_reading(file):
    extension = os.path.splitext(file.filename)[1]
    if file:
        if extension not in current_app.config['ALLOWED_EXTENSIONS']:
            return "File should be pdf or txt"
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
            contents = ''
            for page in pdf_reader.pages:
                contents += page.extract_text() or ""

        else:
            contents = file.read().decode('utf-8')

    return contents



