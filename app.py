from flask import Flask, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge
import PyPDF2
import os,nltk, json
from io import BytesIO
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
import spacy, requests, json

nlp = spacy.load("en_core_web_md")

import http.client


#referencing this file
app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = '/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
app.config['ALLOWED_EXTENSIONS'] = ['.txt', '.pdf']

#when user goes to browser run home + get means get data post means submit data (here we did post)
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods = ['POST'])
def upload():
    try:
        file = request.files['cv']
        if not file:
            return "No file uploaded"
        contents = cv_reading(file)
        new_file = read_api()
        cleaned_cv = clean_data(contents)
        cv_doc = nlp(cleaned_cv)
        similarity_doc = []
        
        for job in new_file["results"]:
            job_desc = job.get("description", "")
            cleaned_file = clean_data(job_desc)
            job_doc = nlp(cleaned_file)
            similarity = cv_doc.similarity(job_doc)
            similarity_doc.append((job,similarity))
        
        similarity_doc.sort(key = lambda x:x[1],reverse= True)
        return render_template('results.html', job_listing = similarity_doc, new_list = new_file["results"])
    except RequestEntityTooLarge:
        return "File is larger than 16 MB"
    

def read_api():
    app_id = "fdc1d9e8"
    app_key = "37d7662bc3ab69a8850995ebc7a6dc6b"
    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data


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
        if extension not in app.config['ALLOWED_EXTENSIONS']:
            return "File should be pdf or txt"
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
            contents = ''
            for page in pdf_reader.pages:
                contents += page.extract_text() or ""

        else:
            contents = file.read().decode('utf-8')
    return contents

    
if __name__ == "__main__":
    app.run(debug= True)

